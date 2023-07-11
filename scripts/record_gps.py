from mardaq.database import MARDB
from mardaq.tables import TABLE
from mardaq.sensors.gps import ADAFRUITGPSHAT
from mardaq.core import load_config, initialize_logger
import time


def main():
    cfg = load_config()
    mdb = MARDB(database_name = 'mysql_test_dep')
    if cfg['sensors']['gps']['enabled'] is False:
        pass
    else:
        table_name = 'gps'
        fields_dtypes = TABLE.GPS.FIELDS_DTYPES
        mdb.create_table(table_name, fields_dtypes)
        gps = ADAFRUITGPSHAT(cfg['sensors']['gps']['sn'])
        while True:
            t1 = time.monotonic()
            mdb.insert_table(table_name, fields_dtypes, gps.get_data())
            t2 = time.monotonic()
            try:
                time.sleep(1-(t2-t1))
            except:
                time.sleep(1)


if __name__ == "__main__":
    main()