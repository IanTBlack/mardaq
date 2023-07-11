from mardaq.database import MARDB
from mardaq.tables import TABLE
from mardaq.sensors.tsg import AtlasTSG
from mardaq.core import load_config
import time


def main():
    cfg = load_config()
    mdb = MARDB(database_name = cfg['deployment'])
    if cfg['sensors']['tsg1']['enabled'] is False:
        pass
    else:
        table_name = 'tsg'
        fields_dtypes = TABLE.TSG.FIELDS_DTYPES
        mdb.create_table(table_name, fields_dtypes)
        tsg = AtlasTSG(cfg['sensors']['tsg1']['sn'])
        while True:
            t1 = time.monotonic()
            tsg.request_data()
            mdb.insert_table(table_name, fields_dtypes, tsg.get_data())
            t2 = time.monotonic()
            try:
                time.sleep(1-(t2-t1))
            except:
                time.sleep(1)


if __name__ == "__main__":
    main()