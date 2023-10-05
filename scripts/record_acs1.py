import time

from mardaq.core import load_config, load_table_structure, load_credentials, console_logger
from mardaq.database import PGDB

from mardaq.sensors.acs import ACS as SENSOR
table_structure_id = 'acs_v3'
table_name = 'acs1'

def main():
    console_log = console_logger(1)
    cfg = load_config('/home/sel/mardaq/config/deployment.cfg')
    sensor_cfg = cfg['sensors'][table_name]
    if sensor_cfg['enabled']:
        fields, pg_dtypes, _ = load_table_structure(cfg['table_structures_location'], table_structure_id)
        __u, __p = load_credentials(cfg['netrc_location'])
        mdb = PGDB(cfg['deployment_id'],user = __u, password = __u)
        mdb.setup_table(table_name, dict(zip(fields,pg_dtypes)))
        sensor = SENSOR(sensor_cfg['dev_file'])
        sensor.connect(sensor_cfg['com_port'])
        while True:
            t1 = time.monotonic()
            try:
                data = sensor.get_data()
                mdb.insert_data(table_name, data)
            except Exception as error:
                console_log.critical(error)
                console_log.critical('Unable to insert ACS data into table.')
                sensor.rs232.clear_buffers()
                time.sleep(0.1)
            t2 = time.monotonic()
            try:
                time.sleep(0.2-(t2-t1))
            except:
                time.sleep(0.2)
    else:
        pass

if __name__ == "__main__":
    main()