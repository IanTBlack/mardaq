import time

from mardaq.core import load_config, load_table_structure, load_credentials
from mardaq.database import PGDB
from mardaq.sensors.gps import ADAFRUITGPSHAT
from mardaq.sensors.flowmeter import OmegaFPR302_Labjack
from mardaq.sensors.tsg import ATLASTSG

from mardaq.components.pump import SHURFLOBAITMASTER
from mardaq.components.valve import ATLANTICBVB4TV

gps_structure = 'adafruit_gps'
gps_table = 'gps1'

pump_structure = 'shurflo'
pump_table = 'pump1'

valve_structure = "atlantic_valve"
valve_table = 'valve1'

flow_structure = "omegafpr302"
flow_table = 'flow1'

tsg_structure = "atlas_tsg"
tsg_table = 'tsg1'



def main():
    cfg = load_config('/home/sel/mardaq/config/deployment.cfg')
    __u, __p = load_credentials(cfg['netrc_location'])
    mdb = PGDB(cfg['deployment_id'], user=__u, password=__u)

    pump_cfg = cfg['sensors'][pump_table]
    if pump_cfg['enabled']:
        pump_fields, pump_dtypes, _ = load_table_structure(cfg['table_structures_location'], pump_structure)
        mdb.setup_table(pump_table, dict(zip(pump_fields, pump_dtypes)))
        pump = SHURFLOBAITMASTER(pump_cfg['sn'])

    valve_cfg = cfg['sensors'][valve_table]
    if valve_cfg['enabled']:
        valve_fields, valve_dtypes, _ = load_table_structure(cfg['table_structures_location'], valve_structure)
        mdb.setup_table(valve_table, dict(zip(valve_fields, valve_dtypes)))
        valve = ATLANTICBVB4TV(valve_cfg['sn'])

    flow_cfg = cfg['sensors'][flow_table]
    if flow_cfg['enabled']:
        flow_fields, flow_dtypes, _ = load_table_structure(cfg['table_structures_location'], flow_structure)
        mdb.setup_table(flow_table, dict(zip(flow_fields, flow_dtypes)))
        flow = OmegaFPR302_Labjack(flow_cfg['sn'],flow_cfg['kfactor'])

    tsg_cfg = cfg['sensors'][tsg_table]
    if tsg_cfg['enabled']:
        tsg_fields, tsg_dtypes, _ = load_table_structure(cfg['table_structures_location'], tsg_structure)
        mdb.setup_table(tsg_table, dict(zip(tsg_fields, tsg_dtypes)))
        tsg = ATLASTSG(tsg_cfg['sn'])

    gps_cfg = cfg['sensors'][gps_table]
    if gps_cfg['enabled']:
        gps_fields, gps_dtypes, _ = load_table_structure(cfg['table_structures_location'], gps_structure)
        mdb.setup_table(gps_table, dict(zip(gps_fields, gps_dtypes)))
        gps = ADAFRUITGPSHAT(gps_cfg['sn'])

    while True:
        t1 = time.monotonic()
        tsg.request_data()
        #mdb.insert_data(pump_table, pump.get_data())
        mdb.insert_data(valve_table, valve.get_data())
        mdb.insert_data(gps_table, gps.get_data())
        mdb.insert_data(flow_table, flow.get_data())
        mdb.insert_data(tsg_table, tsg.get_data(t1))
        t2 = time.monotonic()
        try:
            time.sleep(1-(t2-t1))
        except:
            time.sleep(1)

    else:
        pass


if __name__ == "__main__":
    main()