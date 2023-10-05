import time

from mardaq.core import load_config, load_table_structure, load_credentials
from mardaq.database import PGDB

from mardaq.sensors.tsg import ATLASTSG as SENSOR
table_structure_id = 'atlas_tsg'
table_name = 'tsg1'

def main():
    cfg = load_config('/home/sel/mardaq/config/deployment.cfg')
    sensor_cfg = cfg['sensors'][table_name]
    if sensor_cfg['enabled']:
        fields, pg_dtypes, _ = load_table_structure(cfg['table_structures_location'], table_structure_id)
        __u, __p = load_credentials(cfg['netrc_location'])
        mdb = PGDB(cfg['deployment_id'],user = __u, password = __u)
        mdb.setup_table(table_name, dict(zip(fields,pg_dtypes)))
        sensor = SENSOR(sensor_cfg['sn'])
        while True:
            sensor.request_data()
            t1 = time.monotonic()
            time.sleep(0.6)
            mdb.insert_data(table_name, sensor.get_data())
            t2 = time.monotonic()
            try:
                time.sleep(1-(t2-t1))
            except:
                time.sleep(1)
    else:
        pass



if __name__ == "__main__":
    main()





# def main():
#     cfg = load_config('/home/sel/mardaq/config/deployment.cfg')
#     sensor_cfg = cfg['sensors'][table_name]
#     if sensor_cfg['enabled']:
#         fields, pg_dtypes, _ = load_table_structure(cfg['table_structures_location'], table_structure_id)
#         __u, __p = load_credentials(cfg['netrc_location'])
#         mdb = PGDB(cfg['deployment_id'],user = __u, password = __u)
#         mdb.setup_table(table_name, dict(zip(fields,pg_dtypes)))
#         sensor = SENSOR(sensor_cfg['sn'])
#         while True:
#             t1 = time.monotonic()
#             mdb.insert_data(table_name, sensor.get_data_compensated())
#             t2 = time.monotonic()
#             try:
#                 time.sleep(1-(t2-t1))
#             except:
#                 time.sleep(1)
#     else:
#         pass