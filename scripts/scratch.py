import logging
import netrc
import os
import time
import yaml





with open('/home/sel/mardaq/config/tables.yaml','r') as stream:
    cfg = yaml.safe_load(stream)









table_structure = cfg['adafruit_gps']
fields = list(table_structure.keys())
pg_dtypes = [v['pg_dtype'] for v in table_structure.values()]
np_dtypes = [v['np_dtype'] for v in table_structure.values()]


# import time
# from mardaq.database import PGDB
#
# from mardaq.tables import TABLE
# from mardaq.sensors.gps import ADAFRUITGPSHAT
# from mardaq.sensors.tsg import ATLASTSG
# from mardaq.sensors.acs import ACS
# from mardaq.components.pump import SHURFLOBAITMASTER
# from mardaq.components.valve import ATLANTICBVB4TV
#
#
# gps = ADAFRUITGPSHAT('GPS00001')
# valve = ATLANTICBVB4TV('VALVE00001')
# pump = SHURFLOBAITMASTER('PUMP00001')
# tsg = ATLASTSG('TSG00001')
# acs = ACS('/home/sel/mardaq/config/calibrations/ACS011.DEV')
# acs.connect('/dev/ttyUSB0')
#
# user = 'sel'
# password = 'sel2023'
# with PGDB('test20230825a',user, password) as mdb:
#     mdb.setup_table('gps', TABLE.GPS_ADAFRUIT.FIELDS_DTYPES)
#     mdb.setup_table('pump', TABLE.PUMP.FIELDS_DTYPES)
#     mdb.setup_table('valve', TABLE.VALVE.FIELDS_DTYPES)
#     mdb.setup_table('tsg', TABLE.TSG_ATLAS.FIELDS_DTYPES)
#     mdb.setup_table('acs', TABLE.ACS.FIELDS_DTYPES)
#     for i in range(10):
#         mdb.insert_data('gps',gps.get_data())
#         mdb.insert_data('pump', pump.get_data())
#         mdb.insert_data('valve', valve.get_data())
#         mdb.insert_data('tsg',tsg.get_data())
#         mdb.insert_data('acs',acs.get_data())
#         time.sleep(1)
#     gps_data = mdb.get_data('gps')
#     pump_data = mdb.get_data('pump')
#     valve_data = mdb.get_data('valve')
#     tsg_data = mdb.get_data('tsg')
# acs.rs232._serial.close()