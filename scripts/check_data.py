import subprocess
import time

from mardaq.core import console_logger
from mardaq.core import load_config, load_table_structure, load_credentials, console_logger, load_metadata
from mardaq.database import PGDB

def main():
    console_log = console_logger(1)
    cfg = load_config('/home/sel/mardaq/config/deployment.cfg')
    __u, __p = load_credentials(cfg['netrc_location'])
    mdb = PGDB(cfg['deployment_id'], user=__u, password=__p)
    for table_name in ['gps1','pump1','valve1','flow1','tsg1','acs1']:
        if cfg['sensors'][table_name]['enabled'] is False:
            console_log.info(f"{table_name} was not enabled in the configuration file, so no data check needed.")
            continue
        data = mdb.get_last_hour(table_name)
        num_points = len(data)
        console_log.info(f"{num_points} samples inserted into {table_name} in the last hour.")
        time.sleep(1)

if __name__ == "__main__":
    main()