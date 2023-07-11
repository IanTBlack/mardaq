import time
from mardaq.database import MARDB
from mardaq.tables import TABLE
from mardaq.core import load_config
from mardaq.components.valve import ATLANTICBVB4TV

def main():
    cfg = load_config()
    mdb = MARDB(database_name = cfg['deployment'])
    if cfg['sensors']['valve1']['enabled'] is False:
        pass
    else:
        table_name = 'valve'
        fields_dtypes = TABLE.VALVE.FIELDS_DTYPES
        mdb.create_table(table_name, fields_dtypes)
        valve1 = ATLANTICBVB4TV(cfg['sensors']['valve1']['sn'], channel = cfg['sensors']['valve1']['relay_channel'])
        while True:
            t1 = time.monotonic()
            mdb.insert_table(table_name, fields_dtypes, valve1.get_data())
            t2 = time.monotonic()
            try:
                time.sleep(1-(t2-t1))
            except:
                time.sleep(1)


if __name__ == "__main__":
    main()