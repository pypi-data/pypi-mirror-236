import numpy as np
import os
import xarray as xr

from astrohack._utils._logger._astrohack_logger import _get_astrohack_logger
from astrohack._utils._dio import _load_image_xds
from scipy.interpolate import griddata
from astrohack._utils._constants import clight
from astrohack._utils._tools import _parm_to_list


def _combine_chunk(combine_chunk_params):
    """
    Process a combine chunk
    Args:
        combine_chunk_params: Param dictionary for combine chunk
    """
    logger = _get_astrohack_logger()
    antenna = combine_chunk_params['this_ant']
    ddi_dict = combine_chunk_params['image_mds'][antenna]
    fname = 'combine'
    ddi_list = _parm_to_list(fname, combine_chunk_params['ddi'], ddi_dict, 'ddi')
    print("DDI_LIST:", ddi_list)

    nddi = len(ddi_list)
    out_xds_name = '/'.join([combine_chunk_params['combine_name'], antenna, ddi_list[0]])
    if nddi == 0:
        logger.warning(f'[{fname}]: Nothing to process for {antenna}')
        return
    elif nddi == 1:
        logger.info(f'[{fname}]: {antenna} has a single ddi to be combined, data copied from input file')
        out_xds = ddi_dict[ddi_list[0]]
        out_xds.to_zarr(out_xds_name, mode='w')
    else:
        out_xds = _load_image_xds(combine_chunk_params['image_name'], antenna, ddi_list[0], dask_load=False)
        nddi = len(ddi_list)
        shape = list(out_xds['CORRECTED_PHASE'].values.shape)
        if out_xds.dims['chan'] != 1:
            msg = f'[{fname}]: Only single channel holographies supported'
            logger.error(msg)
            raise Exception(msg)
        npol = shape[2]
        npoints = shape[3]*shape[4]
        amp_sum = np.zeros((npol, npoints))
        pha_sum = np.zeros((npol, npoints))
        for ipol in range(npol):
            amp_sum[ipol, :] = out_xds['AMPLITUDE'].values[0, 0, ipol, :, :].ravel()
            if combine_chunk_params['weighted']:
                pha_sum[ipol, :] = out_xds['CORRECTED_PHASE'].values[0, 0, ipol, :, :].ravel()*amp_sum
            else:
                pha_sum[ipol, :] = out_xds['CORRECTED_PHASE'].values[0, 0, ipol, :, :].ravel()
        wavelength = clight / out_xds.chan.values[0]
        u, v = np.meshgrid(out_xds.u_prime.values * wavelength, out_xds.v_prime.values * wavelength)
        dest_u_axis = u.ravel()
        dest_v_axis = v.ravel()
        for iddi in range(1, nddi):
            logger.info(f'[{fname}]: Regridding {antenna} {ddi_list[iddi]}')
            this_xds = _load_image_xds(combine_chunk_params['image_name'], antenna, ddi_list[iddi], dask_load=False)
            wavelength = clight / this_xds.chan.values[0]
            u, v = np.meshgrid(this_xds.u_prime.values * wavelength, this_xds.v_prime.values * wavelength)
            loca_u_axis = u.ravel()
            loca_v_axis = v.ravel()
            for ipol in range(npol):
                thispha = this_xds['CORRECTED_PHASE'].values[0, 0, ipol, :, :].ravel()
                thisamp = this_xds['AMPLITUDE'].values[0, 0, ipol, :, :].ravel()
                repha = griddata((loca_u_axis, loca_v_axis), thispha, (dest_u_axis, dest_v_axis), method='linear')
                reamp = griddata((loca_u_axis, loca_v_axis), thisamp, (dest_u_axis, dest_v_axis), method='linear')
                amp_sum[ipol, :] += reamp
                if combine_chunk_params['weighted']:
                    pha_sum[ipol, :] += repha*reamp
                else:
                    pha_sum[ipol, :] += repha

        if combine_chunk_params['weighted']:
            phase = pha_sum / amp_sum
        else:
            phase = pha_sum / nddi
        amplitude = amp_sum / nddi

        out_xds['AMPLITUDE'] = xr.DataArray(amplitude.reshape(shape), dims=["time", "chan", "pol", "u_prime", "v_prime"])
        out_xds['CORRECTED_PHASE'] = xr.DataArray(phase.reshape(shape), dims=["time", "chan", "pol", "u_prime", "v_prime"])

        out_xds.to_zarr(out_xds_name, mode='w')

