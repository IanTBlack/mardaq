from mardaq.database import MARDB
from mardaq.tables import TABLE
from mardaq.sensors.flow import OmegaFPR302_Labjack
from mardaq.core import load_config
import time


def main():
    cfg = load_config()
    mdb = MARDB(database_name = cfg['deployment'])
    if cfg['sensors']['flow1']['enabled'] is False:
        pass
    else:
        table_name = 'flow'
        fields_dtypes = TABLE.FLOW.FIELDS_DTYPES
        mdb.create_table(table_name, fields_dtypes)
        flow = OmegaFPR302_Labjack(cfg['sensors']['flow1']['sn'], cfg['sensors']['flow1']['kfactor'])
        while True:
            t1 = time.monotonic()
            mdb.insert_table(table_name, fields_dtypes, flow.get_data())
            t2 = time.monotonic()
            try:
                time.sleep(1-(t2-t1))
            except:
                time.sleep(1)


if __name__ == "__main__":
    main()