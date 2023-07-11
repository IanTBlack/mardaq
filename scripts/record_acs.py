from mardaq.database import MARDB
from mardaq.tables import TABLE
from mardaq.sensors.acs import ACS
from mardaq.core import load_config
import time


def main():
    cfg = load_config()
    mdb = MARDB(database_name = cfg['deployment'])
    if cfg['sensors']['acs']['enabled'] is False:
        pass
    else:
        table_name = 'acs'
        fields_dtypes = TABLE.ACS.FIELDS_DTYPES
        mdb.create_table(table_name, fields_dtypes)
        acs = ACS(cfg['sensors']['acs']['sn'],cfg['sensors']['acs']['cal_file'])
        acs.connect(cfg['sensors']['acs']['com_port'])
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
                data = acs.get_data()
                mdb.insert_table(table_name, fields_dtypes, data)
                t2 = time.monotonic()
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