import numpy as np
import os
import shutil
import xarray as xr

from mardaq.core import load_config, load_table_structure, load_credentials, console_logger, load_metadata
from mardaq.database import PGDB

table_structure_id = 'atlantic_valve'
metadata_id = 'atlantic_valve'
table_name = 'valve1'


def main():
    save_dir = '/home/sel/mardaq/data'
    os.makedirs(save_dir, exist_ok=True)
    console_log = console_logger(1)
    console_log.info(f"Beginning data export for {table_name}.")
    cfg = load_config('/home/sel/mardaq/config/deployment.cfg')
    if cfg['sensors'][table_name]['enabled'] is False:
        console_log.info(f"{table_name} was not enabled in the configuration file, so no export of data needed.")
        exit(0)
    else:
        fields, pg_dtypes, np_dtypes = load_table_structure(cfg['table_structures_location'], table_structure_id)
        fields_nptypes = dict(zip(fields, np_dtypes))
        __u, __p = load_credentials(cfg['netrc_location'])
        mdb = PGDB(cfg['deployment_id'], user=__u, password=__p)
        data = mdb.get_last_hour(table_name)
        if len(data) == 0:
            console_log.critical(f"No data collected in {table_name}")
            exit(0)
        _dict = {}
        for field in fields:
            idx = fields.index(field)
            _list = [v[idx] for v in data]
            _dict[field] = _list

        # Set Data
        ds = xr.Dataset()
        ds = ds.assign_coords({'time': np.array(_dict['time']).astype(fields_nptypes['time'])})

        if 'serial_number' in fields:
            sn = list(np.unique(_dict['serial_number']))
            if len(sn) == 1:
                [sn] = sn
                ds.attrs[f"{table_name}_serial_number"] = sn
            else:
                ds[f"{table_name}_serial_number"] = (
                ('time'), np.array(_dict['serial_number']).astype(fields_nptypes['serial_number']))

        if 'kfactor' in fields:
            kfac = list(np.unique(_dict['kfactor']))
            if len(kfac) == 1:
                [kfac] = kfac
                ds.attrs[f"kfactor"] = kfac
            else:
                ds[f"kfactor"] = (('time'), np.array(_dict['kfactor']).astype(fields_nptypes['kfactor']))

        if 'output_wavelengths' in fields:
            ow = list(np.unique(_dict['output_wavelengths']))
            if len(ow) == 1:
                [ow] = ow
                ds.attrs[f"output_wavelengths"] = ow
            else:
                ds[f"output_wavelengths"] = (
                ('time'), np.array(_dict['output_wavelengths']).astype(fields_nptypes['output_wavelengths']))

        if 'dev_file' in fields:
            df = list(np.unique(_dict['dev_file']))
            if len(df) == 1:
                [df] = df
                ds.attrs[f"dev_file"] = df
            else:
                ds[f"dev_file"] = (('time'), np.array(_dict['dev_file']).astype(fields_nptypes['dev_file']))

        a_vars_2d = ['a_sig', 'a_ref', 'a_offsets', 'a_uncorr', 'delta_t_a', 'a_m']
        if 'wavelength_a' in fields:
            wa = list(np.unique(_dict['wavelength_a']))
            if len(wa) > 1 and len(wa) < 50:  # Assume multiple ACS sensor data.
                ds[f"wavelength_a"] = (('time'), np.array(_dict['wavelength_a']).astype(fields_nptypes['wavelength_a']))
            elif len(wa) > 50:
                ds = ds.assign_coords({'wavelength_a': np.array(wa).astype(fields_nptypes['wavelength_a'])})
                for a_var in a_vars_2d:
                    ds[a_var] = (('time', 'wavelength_a'), np.array(_dict[a_var]).astype(fields_nptypes[a_var]))

        c_vars_2d = ['c_sig', 'c_ref', 'c_offsets', 'c_uncorr', 'delta_t_c', 'c_m']
        if 'wavelength_c' in fields:
            wc = list(np.unique(_dict['wavelength_c']))
            if len(wc) > 1 and len(wa) < 50:
                ds[f"wavelength_c"] = (('time'), np.array(_dict['wavelength_c']).astype(fields_nptypes['wavelength_c']))
            elif len(wc) >= 50:
                ds = ds.assign_coords({'wavelength_c': np.array(wc).astype(fields_nptypes['wavelength_c'])})
                for c_var in c_vars_2d:
                    ds[c_var] = (('time', 'wavelength_c'), np.array(_dict[c_var]).astype(fields_nptypes[c_var]))

        other_vars = [v for v in fields if
                      v != 'time' and v != 'serial_number' and v != 'kfactor' and v != 'wavelength_a' and v != 'wavelength_c']
        vars_1d = [v for v in other_vars if v not in a_vars_2d and v not in c_vars_2d]
        for v in vars_1d:
            ds[v] = (('time'), np.array(_dict[v]).astype(fields_nptypes[v]))

        metadata = load_metadata(cfg['metadata_location'], metadata_id)
        for attr in list(metadata.keys()):
            ds.attrs[attr] = metadata[attr]

        min_time = ds.time.min().dt.strftime('%Y%m%dT%H%M%SZ').item()
        max_time = ds.time.max().dt.strftime('%Y%m%dT%H%M%SZ').item()
        filename = f"{table_name}_{min_time}-{max_time}.nc"
        encoding_dict = {'time': {'units': u'nanoseconds since 1900-01-01'}}
        local_filepath = f"{save_dir}/{filename}"
        ds.to_netcdf(local_filepath, engine='netcdf4', encoding=encoding_dict)
        if os.path.isfile(local_filepath):
            console_log.info(f"Data saved to {local_filepath}.")
        else:
            console_log.error(f"Unable to save data for {table_name}.")

        ext_drives = os.listdir(f'/media/{os.getlogin()}')
        if len(ext_drives) == 0:
            exit(0)
        elif len(ext_drives) == 1:
            [drive] = ext_drives
            drive_path = f'/media/{os.getlogin()}/{drive}'
            ext_data_path = f"{drive_path}/data"
            os.makedirs(ext_data_path, exist_ok=True)
            ext_filepath = f"{ext_data_path}/{filename}"
            shutil.copy(local_filepath, ext_filepath)
            if os.path.isfile(ext_filepath):
                console_log.info(f"Data copied to {ext_filepath}.")
            else:
                console_log.error(f"Unable to save data to external drive for {table_name}.")
        exit(0)


if __name__ == "__main__":
    main()