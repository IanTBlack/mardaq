from mardaq.database import MARDB
from mardaq.tables import TABLE
from mardaq.sensors.acs import ACS
from mardaq.core import load_config
import time
import xarray as xr

cfg = load_config()
acs = ACS(cfg['sensors']['acs']['sn'], cfg['sensors']['acs']['cal_file'])
acs.connect(cfg['sensors']['acs']['com_port'])

fields_dtypes = TABLE.ACS.FIELDS_DTYPES
fields = list(fields_dtypes.keys())







        fp = '/media/sel/flowthrough/data/test.nc'


        _ds_full = None

        time.sleep(3)
        acs.rs232.clear_buffers()
        init_time = time.monotonic()
        while True:
            t1 = time.monotonic()
            if t1-init_time <= 60: # Acquire data to clear buffer, but don't log.
                _ = acs.get_data()  # Get a quick sample to override any runtime warning.
                time.sleep(0.1)
                continue
            try:
            if _ds_full is None:

            else:
                _ds_full = xr.open_dataset(fp)
                data = acs.get_data4nc()
                _new_ds = xr.Dataset()


                awvls = data['a_wavelength']
                cwvls = data['a_wavelength']

                for coord in ['time']:
                    _new_ds = _new_ds.assign_coords({coord: [data[coord]]})
                _new_ds = _new_ds.assign_coords({'wavelength_a': awvls})
                _new_ds = _new_ds.assign_coords({'wavelength_c': cwvls})

                for data_var in ['internal_temperature', 'external_temperature',
                                 't_int',
                                 't_ext', 'pressure_counts', 'frame_len', 'frame_type',
                                 'a_ref_dark', 'a_sig_dark', 'c_ref_dark', 'c_sig_dark']:
                    _new_ds[data_var] = (['time'], [data[data_var]])

                for data_var in ['c','a','c_ref','c_sig','a_ref','a_sig']:
                    if data_var == 'a' or 'a_' in data_var:
                        _new_ds[data_var] = (['time', 'a_wavelength'], [data[data_var]])
                    elif data_var == 'c' or 'c_' in data_var:
                        _new_ds[data_var] = (['time', 'c_wavelength'], [data[data_var]])

                if _ds_full is None:
                    _new_ds.to_netcdf(fp,'w', engine = 'netcdf4'
                else:
                    _appended_ds = xr.concat([_ds_full,_new_ds], dim = ['time','a_wavelength',''])




                t2 = time.monotonic()

                print(t2-t1)
                try:
                    time.sleep(0.1 - (t2-t1))
                except:
                    time.sleep(0.1)
            except:
                time.sleep(0.1)
                print('fail')
                continue



if __name__ == "__main__":
    main()