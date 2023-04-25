from mardaq.core import *
from mardaq.database import MARDB

save_dir = '/home/sel/mardaq/tests/exported_test_data/'

cruise_id = 'TEST_20230424A'
mdb = MARDB(cruise_id)


gps_data = mdb.read_gps()
gps_filepath= os.path.join(save_dir, 'gps.csv')
gps_data.to_csv(gps_filepath)
gps_data.index = pd.to_datetime(gps_data['datetime'])
gps_data = gps_data.drop(columns = ['datetime'])
gps_data = gps_data[['latitude','longitude']]


pump_data = mdb.read_pump()
pump_filepath= os.path.join(save_dir, 'pump.csv')
pump_data.to_csv(pump_filepath)
pump_data.index = pd.to_datetime(pump_data['datetime'])
pump_data = pump_data.drop(columns = ['datetime'])
pump_data = pump_data[['pump_on']]

tsg_data = mdb.read_tsg()
tsg_filepath= os.path.join(save_dir, 'tsg.csv')
tsg_data.to_csv(tsg_filepath)
tsg_data.index = pd.to_datetime(tsg_data['datetime'])
tsg_data = tsg_data.drop(columns = ['datetime'])
tsg_data = tsg_data[['temperature','conductivity']]

valve_data = mdb.read_valve()
valve_filepath= os.path.join(save_dir, 'valve.csv')
valve_data.to_csv(valve_filepath)
valve_data.index = pd.to_datetime(valve_data['datetime'])
valve_data = valve_data.drop(columns = ['datetime'])
valve_data = valve_data[['valve_relay_state']]

df = pd.concat([gps_data,pump_data,tsg_data,valve_data])
binned = df.resample('5S').mean()


binned_filepath = os.path.join(save_dir, "binned_5S.csv")
binned['datetime'] = binned.index
binned = binned.reset_index(drop = True)
binned.to_csv(binned_filepath)

xrnc = binned.set_index(['datetime','latitude','longitude']).to_xarray()