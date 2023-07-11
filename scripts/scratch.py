from mardaq.database import MARDB
from mardaq.tables import TABLE
from mardaq.sensors.gps import ADAFRUITGPSHAT
import time

mdb = MARDB(database_name='test_b')
fields_dtypes = TABLE.ADAFRUITGPSHAT.FIELDS_DTYPES
mdb.create_table('gps',fields_dtypes)
gps = ADAFRUITGPSHAT('sn00001')

for i in range(10):
    mdb.insert_table('gps',fields_dtypes,gps.get_data())
    time.sleep(1)


all_data = mdb.get_data('gps')
single_point = mdb.get_data('gps',method = 'last')