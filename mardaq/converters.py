import ast
import numpy as np
import os
import xarray as xr

from mardaq.tables import TABLE

def dev2xr_acs(dev_parser):
    #Get Calibration Info
    calds = xr.Dataset()
    calds = calds.assign_coords({'temperatures': np.array(dev_parser.t)})
    calds = calds.assign_coords({'wavelengths_a': np.array(dev_parser.lambda_a)})
    calds = calds.assign_coords({'wavelengths_c': np.array(dev_parser.lambda_c)})
    calds['offsets_a'] = (('wavelengths_a'), dev_parser.offset_a)
    calds['offsets_c'] = (('wavelengths_c'), dev_parser.offset_c)
    calds['delta_t_a'] = (('wavelengths_a', 'temperatures'), dev_parser.delta_t_a)
    calds['delta_t_c'] = (('wavelengths_c', 'temperatures'), dev_parser.delta_t_c)
    calds.attrs['title'] = "ACS Factory Calibration"
    calds.attrs['factory_cal_date'] = dev_parser._dev_created_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    calds.attrs['structure_version'] = dev_parser.structure_version_number
    calds.attrs['serial_number'] = dev_parser.serial_number
    calds.attrs['baud_rate'] = dev_parser.baudrate
    calds.attrs['output_wavelengths'] = dev_parser.output_wavelength
    calds.attrs['output_temperatures'] = len(np.array(dev_parser.t))
    calds.attrs['path_length'] = dev_parser.x
    calds.attrs['depth_cal_offset'] = dev_parser.depth_cal_offset
    calds.attrs['depth_cal_scale_factor'] = dev_parser.depth_cal_scale_factor
    calds.attrs['tcal'] = dev_parser.tcal
    calds.attrs['ical'] = dev_parser.ical
    calds.attrs['max_a_noise'] = dev_parser.maxANoise
    calds.attrs['max_c_noise'] = dev_parser.maxCNoise
    calds.attrs['max_a_nonconform'] = dev_parser.maxANonConform
    calds.attrs['max_c_nonconform'] = dev_parser.maxCNonConform
    calds.attrs['max_a_difference'] = dev_parser.maxADifference
    calds.attrs['max_c_difference'] = dev_parser.maxCDifference
    calds.attrs['min_a_counts'] = dev_parser.minACounts
    calds.attrs['min_c_counts'] = dev_parser.minCCounts
    calds.attrs['min_r_counts'] = dev_parser.minRCounts
    calds.attrs['max_temp_sdev'] = dev_parser.maxTempSdev
    calds.attrs['max_depth_sdev'] = dev_parser.maxDepthSdev
    return calds


def table2xr_gps(gps_data):
    fields = list(TABLE.GPS.FIELDS_DTYPES.keys())
    _dict = {}
    for field in fields:
        idx = fields.index(field)
        _dict[field] = [v[idx] for v in gps_data]
    ds = xr.Dataset()
    for coord in ['time']:
        ds = ds.assign_coords({coord:_dict[coord]})
    for data_var in ['latitude','longitude','cog','sog','gps_time','gps_status','nmea_string']:
        ds[data_var] = (['time'],_dict[data_var])
        if data_var in ['gps_string','nmea_string']:
            ds[data_var] = ds[data_var].astype(str)
    for attr in ['serial_number']:
        serial_numbers = np.unique(_dict[attr])
        if len(serial_numbers) != 1:
            raise NotImplementedError('No handling for multiple SNs implemented (yet).')
        else:
            [sn] = serial_numbers
            ds.attrs['gps_serial_number'] = str(sn)
    return ds



def table2xr_acs(acs_data):
    fields = list(TABLE.ACS.FIELDS_DTYPES.keys())
    _dict = {}
    for field in fields:
        idx = fields.index(field)
        _dict[field] = [v[idx] for v in acs_data]
        if field in ['a','c','a_sig','a_ref','c_sig','c_ref','wavelength_c','wavelength_a']:
            _dict[field] = [ast.literal_eval(v) for v in _dict[field]]

    # Get unique items.
    awvls = np.unique(_dict['wavelength_a'])
    cwvls = np.unique(_dict['wavelength_c'])
    output_wavelengths = int(np.unique(_dict['output_wavelengths']))
    [dev_file] = np.unique(_dict['dev_file'])
    [sn] = np.unique(_dict['serial_number'])

    ds = xr.Dataset()

    # Assign coords
    for coord in ['time']:
        ds = ds.assign_coords({coord:_dict[coord]})
    ds = ds.assign_coords({'wavelength_a':awvls})
    ds = ds.assign_coords({'wavelength_c':cwvls})

    # Assign 2D data variables.
    for data_var in ['a','c','a_sig','a_ref','c_sig','c_ref']:
        if data_var == 'a' or 'a_' in data_var:
            ds[data_var] = (['time','wavelength_a'],_dict[data_var])
        elif data_var == 'c' or 'c_' in data_var:
            ds[data_var] = (['time', 'wavelength_c'], _dict[data_var])


    # Assign 1D data variables.
    for data_var in ['internal_temperature','external_temperature','outside_cal_range','time_since_power_ms','t_int',
                     't_ext', 'pressure_counts','frame_length','frame_type',
                     'a_ref_dark','a_sig_dark','c_ref_dark','c_sig_dark']:
        ds[data_var] = (['time'],_dict[data_var])


    # Assign attributes.
    ds.attrs['output_wavelengths'] = output_wavelengths
    ds.attrs['acs_serial_number'] = sn
    ds.attrs['acs_dev_file'] = dev_file
    return ds


def table2xr_tsg(tsg_data):
    fields = list(TABLE.TSG.FIELDS_DTYPES.keys())
    _dict = {}
    for field in fields:
        idx = fields.index(field)
        _dict[field] = [v[idx] for v in tsg_data]
    ds = xr.Dataset()
    for coord in ['time']:
        ds = ds.assign_coords({coord:_dict[coord]})
    for data_var in ['temperature','conductivity','practical_salinity']:
        ds[data_var] = (['time'],[float(v) if v is not None else np.nan for v in _dict[data_var]])
        ds[data_var] = ds[data_var].where(ds[data_var] is not None, np.nan)
    for attr in ['serial_number']:
        serial_numbers = np.unique(_dict[attr])
        if len(serial_numbers) != 1:
            raise NotImplementedError('No handling for multiple SNs implemented (yet).')
        else:
            [sn] = serial_numbers
            ds.attrs['tsg_serial_number'] = str(sn)
    return ds


def table2xr_valve(valve_data):
    fields = list(TABLE.VALVE.FIELDS_DTYPES.keys())
    _dict = {}
    for field in fields:
        idx = fields.index(field)
        _dict[field] = [v[idx] for v in valve_data]
    ds = xr.Dataset()
    for coord in ['time']:
        ds = ds.assign_coords({coord:_dict[coord]})
    for data_var in ['valve_relay_state','seawater_state']:
        ds[data_var] = (['time'],_dict[data_var])
        ds[data_var] = ds[data_var].astype('int16')
    for attr in ['serial_number']:
        serial_numbers = np.unique(_dict[attr])
        if len(serial_numbers) != 1:
            raise NotImplementedError('No handling for multiple SNs implemented (yet).')
        else:
            [sn] = serial_numbers
            ds.attrs['valve_serial_number'] = str(sn)
    return ds



def table2xr_pump(pump_data):
    fields = list(TABLE.PUMP.FIELDS_DTYPES.keys())
    _dict = {}
    for field in fields:
        idx = fields.index(field)
        _dict[field] = [v[idx] for v in pump_data]
    ds = xr.Dataset()
    for coord in ['time']:
        ds = ds.assign_coords({coord:_dict[coord]})
    for data_var in ['pump_relay_state','pump_on']:
        ds[data_var] = (['time'],_dict[data_var])
        ds[data_var] = ds[data_var].astype('int16')
    for attr in ['serial_number']:
        serial_numbers = np.unique(_dict[attr])
        if len(serial_numbers) != 1:
            raise NotImplementedError('No handling for multiple SNs implemented (yet).')
        else:
            [sn] = serial_numbers
            ds.attrs['pump_serial_number'] = str(sn)
    return ds


def table2xr_flow(flow_data):
    fields = list(TABLE.FLOW.FIELDS_DTYPES.keys())
    _dict = {}
    for field in fields:
        idx = fields.index(field)
        _dict[field] = [v[idx] for v in flow_data]
    ds = xr.Dataset()
    for coord in ['time']:
        ds = ds.assign_coords({coord:_dict[coord]})
    for data_var in ['cumulative_pulses']:
        ds[data_var] = (['time'],_dict[data_var])
        ds[data_var] = ds[data_var].astype('int64')
    for data_var in ['kfactor','cumulative_ml','ml_per_min']:
        ds[data_var] = (['time'],_dict[data_var])
    for attr in ['serial_number']:
        serial_numbers = np.unique(_dict[attr])
        if len(serial_numbers) != 1:
            raise NotImplementedError('No handling for multiple SNs implemented (yet).')
        else:
            [sn] = serial_numbers
            ds.attrs['flow_serial_number'] = str(sn)
    return ds