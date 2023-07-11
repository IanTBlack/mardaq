import time
from mardaq.database import MARDB
from mardaq.tables import TABLE
from mardaq.core import load_config
from mardaq.components.pump import SHURFLOBAITMASTER

def main():
    cfg = load_config()
    mdb = MARDB(database_name = cfg['deployment'])
    if cfg['sensors']['pump']['enabled'] is False:
        pass
    else:
        table_name = 'pump'
        fields_dtypes = TABLE.PUMP.FIELDS_DTYPES
        mdb.create_table(table_name, fields_dtypes)
        pump = SHURFLOBAITMASTER(cfg['sensors']['pump']['sn'],channel = cfg['sensors']['pump']['relay_channel'])
        while True:
            t1 = time.monotonic()
            mdb.insert_table(table_name, fields_dtypes, pump.get_data())
            t2 = time.monotonic()
            try:
                time.sleep(1-(t2-t1))
            except:
                time.sleep(1)


if __name__ == "__main__":
    main()