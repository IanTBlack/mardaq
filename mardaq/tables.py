class TABLE:

    class GPS:
        FIELDS_DTYPES = {'time':'DATETIME(6)',
                         'latitude': 'FLOAT',
                         'longitude': 'FLOAT',
                         'cog': 'FLOAT',
                         'sog': 'FLOAT',
                         'gps_time': 'DATETIME(6)',
                         'gps_status': 'VARCHAR(10)',
                         'nmea_string': 'VARCHAR(255)',
                         'serial_number': 'VARCHAR(64)'}


    class PUMP:
        FIELDS_DTYPES = {'time':'DATETIME(6)',
                         'pump_relay_state': 'INT',
                         'pump_on': 'INT',
                         'serial_number': 'VARCHAR(64)'}


    class VALVE:
        FIELDS_DTYPES = {'time':'DATETIME(6)',
                         'valve_relay_state': 'INT',
                         'seawater_state': 'INT',
                         'serial_number': 'VARCHAR(64)'}


    class ACS:
        FIELDS_DTYPES = {'time': 'DATETIME(6)',
                         'a': 'JSON',
                         'c': 'JSON',
                         'wavelength_a': 'JSON',
                         'wavelength_c': 'JSON',
                         'internal_temperature': 'FLOAT',
                         'external_temperature': 'FLOAT',
                         'outside_cal_range': 'BOOLEAN',
                         'output_wavelengths': 'INT',
                         'time_since_power_ms': 'INT',
                         't_int': 'INT',
                         't_ext': 'INT',
                         'pressure_counts': 'INT',
                         'frame_length':'INT',
                         'frame_type':'INT',
                         'a_ref_dark': 'INT',
                         'a_sig_dark': 'INT',
                         'c_ref_dark': 'INT',
                         'c_sig_dark': 'INT',
                         'a_ref': 'JSON',
                         'a_sig': 'JSON',
                         'c_ref': 'JSON',
                         'c_sig': 'JSON',
                         'dev_file':'VARCHAR(255)',
                         'serial_number': 'VARCHAR(32)'}

    class TSG:
        FIELDS_DTYPES = {'time':'DATETIME(6)',
                         'temperature': 'FLOAT',
                         'conductivity': 'FLOAT',
                         'practical_salinity': 'FLOAT',
                         'serial_number': 'VARCHAR(64)'}

    class FLOW:
        FIELDS_DTYPES = {'time':'DATETIME(6)',
                         'kfactor': 'FLOAT',
                         'cumulative_pulses': 'INT',
                         'cumulative_ml': 'FLOAT',
                         'ml_per_min': 'FLOAT',
                         'serial_number': 'VARCHAR(64)'}