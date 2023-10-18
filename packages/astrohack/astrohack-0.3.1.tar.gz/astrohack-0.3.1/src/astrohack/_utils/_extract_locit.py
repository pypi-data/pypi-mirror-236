import numpy as np

from casacore import tables as ctables
from astropy.coordinates import SkyCoord, CIRS
from astropy.time import Time
import astropy.units as units
import xarray as xr
from prettytable import PrettyTable

from astrohack._utils._logger._astrohack_logger import _get_astrohack_logger
from astrohack._utils._tools import _casa_time_to_mjd, _rad_to_deg_str
from astrohack._utils._conversion import _convert_unit
from astrohack._utils._constants import figsize, twopi, notavail
from astrohack._utils._dio import _write_meta_data
from astrohack._utils._locit_commons import _open_telescope, _compute_antenna_relative_off, _get_telescope_lat_lon_rad
from astrohack._utils._locit_commons import _plot_boxes_limits_and_labels
from astrohack._utils._plot_commons import _create_figure_and_axes, _close_figure, _scatter_plot
from astrohack._utils._locit_commons import _plot_antenna_position


def _extract_antenna_data(fname, extract_locit_parms):
    """
    Extract antenna information from the ANTENNA sub table of the cal table
    Args:
        fname: Caller
        extract_locit_parms: input_parameters to extract_locit
    Returns:
    Antenna dictionary
    """
    logger = _get_astrohack_logger()
    cal_table = extract_locit_parms['cal_table']
    ant_table = ctables.table(cal_table + '::ANTENNA', readonly=True, lockoptions={'option': 'usernoread'}, ack=False)
    ant_off = ant_table.getcol('OFFSET')
    ant_pos = ant_table.getcol('POSITION')
    ant_mnt = ant_table.getcol('MOUNT')
    ant_nam = ant_table.getcol('NAME')
    ant_sta = ant_table.getcol('STATION')
    ant_typ = ant_table.getcol('TYPE')
    ant_table.close()

    n_ant_orig = ant_off.shape[0]
    ant_pos_corrected = ant_pos + ant_off
    ant_rad = np.sqrt(ant_pos_corrected[:, 0] ** 2 + ant_pos_corrected[:, 1] ** 2 + ant_pos_corrected[:, 2] ** 2)
    ant_lat = np.arcsin(ant_pos_corrected[:, 2] / ant_rad)
    ant_lon = -np.arccos(ant_pos_corrected[:, 0] / (ant_rad * np.cos(ant_lat)))

    if extract_locit_parms['ant'] == 'all':
        ant_list = ant_nam
    else:
        ant_list = extract_locit_parms['ant']

    ant_dict = {}
    error = False
    for i_ant in range(n_ant_orig):
        this_name = ant_nam[i_ant]
        if this_name in ant_list:
            if ant_mnt[i_ant] != 'ALT-AZ':
                logger.error(f'[{fname}]: Antenna {this_name} has a non supported mount type: {ant_mnt[i_ant]}')
                error = True
            if ant_typ[i_ant] != 'GROUND-BASED':
                error = True
                logger.error(f'[{fname}]: Antenna {this_name} is not ground based which is currently not supported')
            if error:
                pass
            else:
                antenna = {'id': i_ant, 'name': this_name, 'station': ant_sta[i_ant],
                           'geocentric_position': ant_pos[i_ant], 'longitude': ant_lon[i_ant],
                           'latitude': ant_lat[i_ant], 'radius': ant_rad[i_ant], 'offset': ant_off[i_ant]}
                ant_dict[i_ant] = antenna

    if error:
        msg = f'[{fname}]: Unsupported antenna characteristics'
        logger.error(msg)
        raise Exception(msg)

    extract_locit_parms['ant_dict'] = ant_dict
    extract_locit_parms['full_antenna_list'] = ant_nam


def _extract_spectral_info(fname, extract_locit_parms):
    """
    Extract spectral information from the SPECTRAL_WINDOW sub table of the cal table
    Args:
        fname: Caller
        extract_locit_parms: input_parameters to extract_locit

    Returns:
    DDI dictionary
    """
    logger = _get_astrohack_logger()
    cal_table = extract_locit_parms['cal_table']
    spw_table = ctables.table(cal_table+'::SPECTRAL_WINDOW', readonly=True, lockoptions={'option': 'usernoread'}, ack=False)
    ref_freq = spw_table.getcol('REF_FREQUENCY')
    n_chan = spw_table.getcol('NUM_CHAN')
    bandwidth = spw_table.getcol('CHAN_WIDTH')
    spw_table.close()
    n_ddi = len(ref_freq)
    error = False
    if extract_locit_parms['ddi'] == 'all':
        ddi_list = range(n_ddi)
    else:
        if isinstance(extract_locit_parms['ddi'], int):
            ddi_list = [extract_locit_parms['ddi']]
        else:
            ddi_list = extract_locit_parms['ddi']

    ddi_dict = {}
    for i_ddi in ddi_list:
        if n_chan[i_ddi] != 1:
            error = True
            msg = f'[{fname}]: DDI {i_ddi} has {n_chan[i_ddi]}, which is not supported'
            logger.error(msg)
        else:
            ddi_dict[i_ddi] = {'id': i_ddi, 'frequency': ref_freq[i_ddi], 'bandwidth': bandwidth[i_ddi]}

    if error:
        msg = f'[{fname}]: Unsupported DDI characteristics'
        logger.error(msg)
        raise Exception(msg)
    extract_locit_parms['ddi_dict'] = ddi_dict


def _extract_source_and_telescope(fname, extract_locit_parms):
    """
    Extract source and telescope  information from the FIELD and OBSERVATION sub tables of the cal table
    Args:
        fname: Caller
        extract_locit_parms: input_parameters to extract_locit

    Returns:
    Writes dict to a json file
    """
    cal_table = extract_locit_parms['cal_table']
    basename = extract_locit_parms['locit_name']
    src_table = ctables.table(cal_table+'::FIELD', readonly=True, lockoptions={'option': 'usernoread'}, ack=False)
    src_ids = src_table.getcol('SOURCE_ID')
    phase_center_fk5 = src_table.getcol('PHASE_DIR')[:, 0, :]
    src_name = src_table.getcol('NAME')
    src_table.close()
    n_src = len(src_ids)

    phase_center_fk5[:, 0] = np.where(phase_center_fk5[:, 0] < 0, phase_center_fk5[:, 0]+twopi,
                                        phase_center_fk5[:, 0])

    obs_table = ctables.table(cal_table+'::OBSERVATION', readonly=True, lockoptions={'option': 'usernoread'}, ack=False)
    time_range = _casa_time_to_mjd(obs_table.getcol('TIME_RANGE')[0])
    telescope_name = obs_table.getcol('TELESCOPE_NAME')[0]
    obs_table.close()

    mid_time = Time((time_range[-1]+time_range[0])/2, scale='utc', format='mjd')

    astropy_fk5 = SkyCoord(phase_center_fk5[:, 0], phase_center_fk5[:, 1], unit=units.rad, frame='fk5')
    astropy_precessed = astropy_fk5.transform_to(CIRS(obstime=mid_time))
    phase_center_precessed = np.ndarray((n_src, 2))
    phase_center_precessed[:, 0] = astropy_precessed.ra
    phase_center_precessed[:, 1] = astropy_precessed.dec
    phase_center_precessed *= _convert_unit('deg', 'rad', 'trigonometric')

    src_dict = {}
    for i_src in range(n_src):
        src_id = int(src_ids[i_src])
        src_dict[src_id] = {'id': src_id, 'name': src_name[i_src], 'fk5': phase_center_fk5[i_src].tolist(),
                            'precessed': phase_center_precessed[i_src].tolist()}

    obs_dict = {'src_dict': src_dict, 'time_range': time_range.tolist(), 'telescope_name': telescope_name}

    _write_meta_data("/".join([basename, ".observation_info"]), obs_dict)
    extract_locit_parms['telescope_name'] = telescope_name
    return telescope_name, n_src


def _extract_antenna_phase_gains(fname, extract_locit_parms):
    """
    Extract antenna based phase gains from the cal table
    Args:
        fname: Caller
        extract_locit_parms: input_parameters to extract_locit

    Returns:
    Reference antenna
    """
    logger = _get_astrohack_logger()

    cal_table = extract_locit_parms['cal_table']
    basename = extract_locit_parms['locit_name']

    obs_table = ctables.table(cal_table + '::OBSERVATION', readonly=True, lockoptions={'option': 'usernoread'}, ack=False)
    telescope_name = obs_table.getcol('TELESCOPE_NAME')[0]
    obs_table.close()

    main_table = ctables.table(cal_table, readonly=True, lockoptions={'option': 'usernoread'}, ack=False)

    antenna1 = main_table.getcol('ANTENNA1')
    antenna2 = main_table.getcol('ANTENNA2')
    gain_time = _casa_time_to_mjd(main_table.getcol('TIME'))
    gains = main_table.getcol('CPARAM')
    fields = main_table.getcol('FIELD_ID')
    spw_id = main_table.getcol('SPECTRAL_WINDOW_ID')
    flagged = main_table.getcol('FLAG')

    main_table.close()
    n_gains = len(gains)

    ref_antennas, counts = np.unique(antenna2, return_counts=True)
    n_refant = len(ref_antennas)
    if n_refant > 1:
        i_best_ant = np.argmax(counts)
        fraction_best = counts[i_best_ant]/n_gains
        if fraction_best < 0.5:
            logger.warning(f'[{fname}]: The best reference Antenna only covers {100*fraction_best:.1f}% of the data')
        for i_refant in range(n_refant):
            if i_refant != i_best_ant:
                logger.info(f'[{fname}]: Discarding gains derived with antenna '
                            f'{extract_locit_parms["full_antenna_list"][ref_antennas[i_refant]]}'
                            f' as reference ({100*counts[i_refant]/n_gains:.2f}% of the data)')
                sel_refant = antenna2 != ref_antennas[i_refant]
                antenna2 = antenna2[sel_refant]
                antenna1 = antenna1[sel_refant]
                gain_time = gain_time[sel_refant]
                gains = gains[sel_refant]
                fields = fields[sel_refant]
                spw_id = spw_id[sel_refant]
                flagged = flagged[sel_refant]
        ref_antenna = ref_antennas[i_best_ant]
    else:
        # No data to discard we can go on and compute the phase gains
        ref_antenna = ref_antennas[0]

    # Calibration tables do not retain a polarization sub table, hence we are going to infer the polarizations present
    # from the telescope
    if 'VLA' in telescope_name or telescope_name == 'VLBA':
        polarization_scheme = ['R', 'L']
    elif 'ALMA' == telescope_name:
        polarization_scheme = ['X', 'Y']
    else:
        msg = f'Unrecognized telescope {extract_locit_parms["telescope_name"]}'
        logger.error(msg)
        raise Exception(msg)

    n_pol = gains.shape[2]
    if n_pol != 2:
        msg = f'Calibration table has {n_pol} polarizations, which is not supported'
        logger.erro(msg)
        raise Exception(msg)

    used_sources = []
    extract_locit_parms['reference_antenna'] = extract_locit_parms['full_antenna_list'][ref_antenna]
    phase_gains = np.angle(gains)
    for ant_id, antenna in extract_locit_parms['ant_dict'].items():
        ant_sel = antenna1 == ant_id
        ant_time = gain_time[ant_sel]
        ant_field = fields[ant_sel]
        ant_phase_gains = phase_gains[ant_sel]
        ant_spw_id = spw_id[ant_sel]
        ant_flagged = flagged[ant_sel]
        if ant_id == ref_antenna:
            antenna['reference'] = True
        else:
            antenna['reference'] = False

        for ddi_id, ddi in extract_locit_parms['ddi_dict'].items():
            this_ddi_xds = xr.Dataset()
            ddi_sel = ant_spw_id == ddi_id
            ddi_gains = ant_phase_gains[ddi_sel]
            ddi_time = ant_time[ddi_sel]
            ddi_field = ant_field[ddi_sel]
            ddi_not_flagged = np.invert(ant_flagged[ddi_sel])

            coords = {}
            for i_pol in range(n_pol):
                timekey = f'p{i_pol}_time'
                coords[timekey] = ddi_time[ddi_not_flagged[:, 0, i_pol]]
                this_ddi_xds[f'P{i_pol}_PHASE_GAINS'] = xr.DataArray(ddi_gains[ddi_not_flagged[:, 0, i_pol], 0, i_pol],
                                                                     dims=timekey)
                this_ddi_xds[f'P{i_pol}_FIELD_ID'] = xr.DataArray(ddi_field[ddi_not_flagged[:, 0, i_pol]], dims=timekey)
                used_sources.extend(ddi_field[ddi_not_flagged[:, 0, i_pol]])

            this_ddi_xds.attrs['frequency'] = ddi['frequency']
            this_ddi_xds.attrs['bandwidth'] = ddi['bandwidth']
            this_ddi_xds.attrs['polarization_scheme'] = polarization_scheme
            outname = "/".join([basename, 'ant_'+antenna['name'], f'ddi_{ddi["id"]}'])
            this_ddi_xds = this_ddi_xds.assign_coords(coords)
            this_ddi_xds.to_zarr(outname, mode="w", compute=True, consolidated=True)
        _write_meta_data("/".join([basename, 'ant_'+antenna['name'], ".antenna_info"]), antenna)
    extract_locit_parms['used_sources'] = np.unique(np.array(used_sources))
    return


def _plot_source_table(filename, src_dict, label=True, precessed=False, obs_midpoint=None, display=True,
                       figure_size=figsize, dpi=300):
    """ Backend function for plotting the source table
    Args:
        filename: Name for the png plot file
        src_dict: The dictionary containing the observed sources
        label: Add source labels
        precessed: Plot sources with precessed coordinates
        obs_midpoint: Time to which precesses the coordiantes
        display: Display plots in matplotlib
        figure_size: plot dimensions in inches
        dpi: Dots per inch (plot resolution)
    """
    logger = _get_astrohack_logger()
    n_src = len(src_dict)
    radec = np.ndarray((n_src, 2))
    name = []
    if precessed:
        if obs_midpoint is None:
            msg = 'Observation midpoint is missing'
            logger.error(msg)
            raise Exception(msg)
        coorkey = 'precessed'
        time = Time(obs_midpoint, format='mjd')
        title = f'Coordinates precessed to {time.iso}'
    else:
        coorkey = 'fk5'
        title = 'FK5 reference frame'

    for i_src, src in src_dict.items():
        radec[int(i_src)] = src[coorkey]
        name.append(src['name'])

    fig, ax = _create_figure_and_axes(figure_size, [1, 1])
    radec[:, 0] *= _convert_unit('rad', 'hour', 'trigonometric')
    radec[:, 1] *= _convert_unit('rad', 'deg', 'trigonometric')

    xlabel = 'Right Ascension [h]'
    ylabel = 'Declination [\u00b0]'
    if label:
        labels = name
    else:
        labels = None

    _scatter_plot(ax, radec[:, 0], xlabel, radec[:, 1], ylabel, title=None, labels=labels, xlim=[-0.5, 24.5],
                  ylim=[-95, 95])

    _close_figure(fig, title, filename, dpi, display)
    return


def _plot_array_configuration(ant_dict, telescope_name, parm_dict):
    """ backend for plotting array configuration

    Args:
        ant_dict: Dictionary containing antenna information
        telescope_name: Name of the telescope used in observations
        parm_dict: Parameter dictionary crafted by the calling function
    """

    telescope = _open_telescope(telescope_name)
    stations = parm_dict['stations']
    display = parm_dict['display']
    figure_size = parm_dict['figuresize']
    dpi = parm_dict['dpi']
    filename = parm_dict['destination'] + '/locit_antenna_positions.png'
    length_unit = parm_dict['unit']
    box_size = parm_dict['box_size']  # In user input unit
    plot_zoff = parm_dict['zoff']

    fig, axes = _create_figure_and_axes(figure_size, [1, 2], default_figsize=[10, 5])

    len_fac = _convert_unit('m', length_unit, 'length')

    inner_ax = axes[1]
    outer_ax = axes[0]

    tel_lon, tel_lat, tel_rad = _get_telescope_lat_lon_rad(telescope)

    for antenna in ant_dict.values():
        ew_off, ns_off, el_off, _ = _compute_antenna_relative_off(antenna, tel_lon, tel_lat, tel_rad, len_fac)
        text = f'  {antenna["name"]}'
        if stations:
            text += f'@{antenna["station"]}'
        if plot_zoff:
            text += f' {el_off:.1f} {length_unit}'
        _plot_antenna_position(outer_ax, inner_ax, ew_off, ns_off, text, box_size)

    # axes labels
    xlabel = f'East [{length_unit}]'
    ylabel = f'North [{length_unit}]'

    _plot_boxes_limits_and_labels(outer_ax, inner_ax, xlabel, ylabel, box_size, 'Outer array', 'Inner array')

    title = f'{len(ant_dict.keys())} antennas during observation'
    _close_figure(fig, title, filename, dpi, display)
    return


def _print_array_configuration(params, ant_dict, telescope_name):
    """ Backend for printing the array configuration onto a table

    Args:
        params: Parameter dictionary crafted by the calling function
        ant_dict: Parameter dictionary crafted by the calling function
        telescope_name: Name of the telescope used in observations
    """
    telescope = _open_telescope(telescope_name)
    relative = params['relative']

    print(f"\n{telescope_name} antennas, # of antennas {len(ant_dict.keys())}:")
    table = PrettyTable()
    table.align = 'c'
    if relative:
        nfields = 5
        table.field_names = ['Name', 'Station', 'East [m]', 'North [m]', 'Elevation [m]', 'Distance [m]']
        tel_lon, tel_lat, tel_rad = _get_telescope_lat_lon_rad(telescope)
    else:
        nfields = 4
        table.field_names = ['Name', 'Station', 'Longitude', 'Latitude', 'Radius [m]']

    for ant_name in telescope.ant_list:
        ant_key = 'ant_'+ant_name
        if ant_key in ant_dict:
            antenna = ant_dict[ant_key]
            if antenna['reference']:
                ant_name += ' (ref)'
            row = [ant_name, antenna['station']]
            if relative:
                offsets = _compute_antenna_relative_off(antenna, tel_lon, tel_lat, tel_rad)
                row.extend([f'{offsets[0]:.4f}', f'{offsets[1]:.4f}', f'{offsets[2]:.4f}', f'{offsets[3]:.4f}'])
            else:
                row.extend([_rad_to_deg_str(antenna['longitude']),  _rad_to_deg_str(antenna['latitude']),
                           f'{antenna["radius"]:.4f}'])
            table.add_row(row)
        else:
            row = [ant_name]
            for i_field in range(nfields):
                row.append(notavail)
            table.add_row(row)

    print(table)
    return


