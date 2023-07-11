import os
import numpy as np
import xarray as xr
from mardaq.database import MARDB
from mardaq.core import load_config
from mardaq.tables import TABLE
from mardaq.sensors.acs import ACS
from mardaq.converters import table2xr_gps, table2xr_acs, dev2xr_acs, table2xr_tsg, table2xr_valve, table2xr_pump, table2xr_flow

def main():
    folder = '/media/sel/flowthrough/data/netcdf/'
    os.makedirs(folder,exist_ok=True)

    cfg = load_config()
    mdb = MARDB(database_name = cfg['deployment'])

    ACSParser = ACS(cfg['sensors']['acs']['sn'], cfg['sensors']['acs']['cal_file'])
    acs_cal_ds = dev2xr_acs(ACSParser)
    acs_ds = table2xr_acs(mdb.get_data('acs'))  # ACS Data

    tsg_ds = table2xr_tsg(mdb.get_data('tsg'))
    gps_ds = table2xr_gps(mdb.get_data('gps'))
    valve_ds = table2xr_valve(mdb.get_data('valve'))
    pump_ds = table2xr_pump(mdb.get_data('pump'))
    flow_ds = table2xr_flow(mdb.get_data('flow'))






    grouped_fp = os.path.join(folder, f"grouped_{cfg['deployment'].lower()}.nc")
    export2nc_grouped(gps_ds, acs_cal_ds, acs_ds, tsg_ds, valve_ds, pump_ds, flow_ds, grouped_fp)

    combo_fp = os.path.join(folder, f"combo_{cfg['deployment'].lower()}.nc")
    export2nc_combo(gps_ds, acs_cal_ds, acs_ds, tsg_ds, valve_ds, pump_ds, flow_ds, combo_fp)


    print('Conversion to netCDF complete!')

def export2nc_grouped(gps_ds, acs_cal_ds, acs_ds, tsg_ds, valve_ds, pump_ds, flow_ds, save_filepath):
    ds = xr.Dataset()
    ds.to_netcdf(save_filepath,'w', engine = 'netcdf4')
    gps_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4',group = 'gps_data')
    acs_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'acs_data')
    acs_cal_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'acs_factory_calibration')
    valve_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'filtration_data')
    tsg_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'tsg_data')
    pump_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'pump_data')
    flow_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'flow_data')
    if os.path.isfile(save_filepath):
        return True


def export2nc_combo(gps_ds, acs_cal_ds, acs_ds, tsg_ds, valve_ds, pump_ds, flow_ds, save_filepath):
    combo = xr.concat([gps_ds, acs_ds, tsg_ds, valve_ds, pump_ds, flow_ds], dim = 'time')
    combo.to_netcdf(save_filepath,'w', engine = 'netcdf4')
    acs_cal_ds.to_netcdf(save_filepath,'a',engine = 'netcdf4', group = 'acs_factory_calibration')
    if os.path.isfile(save_filepath):
        return True


#
# def export2nc_tsg(tsg_ds, save_filepath):
#     tsg_ds.to_netcdf(save_filepath,'w', engine = 'netcdf4')
#     if os.path.isfile(save_filepath):
#         return True
#
#
# def export2nc_gps(gps_ds, save_filepath):
#     gps_ds.to_netcdf(save_filepath,'w', engine = 'netcdf4')
#     if os.path.isfile(save_filepath):
#         return True
#
# def export2nc_valve(gps_ds, save_filepath):
#     gps_ds.to_netcdf(save_filepath,'w', engine = 'netcdf4')
#     if os.path.isfile(save_filepath):
#         return True
#


if __name__ == "__main__":
    main()