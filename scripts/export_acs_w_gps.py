import os
import numpy as np
import xarray as xr
from mardaq.database import MARDB
from mardaq.core import load_config
from mardaq.tables import TABLE
from mardaq.sensors.acs import ACS
from mardaq.converters import table2xr_gps, table2xr_acs, dev2xr_acs, table2xr_tsg, table2xr_valve

def main():
    cfg = load_config()
    mdb = MARDB(database_name = cfg['deployment'])

    ACSParser = ACS(cfg['sensors']['acs']['sn'], cfg['sensors']['acs']['cal_file'])
    cal_ds = dev2xr_acs(ACSParser)
    gps_ds = table2xr_gps(mdb.get_data('gps'))  # Nav Data
    acs_ds = table2xr_acs(mdb.get_data('acs'))  # ACS Data
    tsg_ds = table2xr_tsg(mdb.get_data('tsg'))
    valve_ds = table2xr_valve(mdb.get_data('valve'))

    folder = '/media/sel/flowthrough/data/netcdf/'
    os.makedirs(folder,exist_ok=True)
    filepath = os.path.join(folder, f"acs_{cfg['deployment'].lower()}.nc")
    export2nc(gps_ds, acs_ds, cal_ds, valve_ds, tsg_ds, filepath)
    print('Conversion to netCDF complete!')

def export2nc(gps_ds, acs_ds, cal_ds, valve_ds, tsg_ds, save_filepath):
    ds = xr.Dataset()
    ds.to_netcdf(save_filepath,'w', engine = 'netcdf4')
    gps_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4',group = 'gps_data')
    acs_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'acs_data')
    cal_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'acs_factory_calibration')
    valve_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'filtration_data')
    tsg_ds.to_netcdf(save_filepath,'a', engine = 'netcdf4', group = 'tsg_data')
    if os.path.isfile(save_filepath):
        return True




if __name__ == "__main__":
    main()