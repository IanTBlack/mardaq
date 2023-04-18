from mardaq.core import *
from mardaq.database import MARDB
from mardaq.pump import ShurfloBaitmaster
from mardaq.valve import AtlanticBVB4TV
from mardaq.gps import AdafruitHAT
from mardaq.tsg import AtlasTSG
from mardaq.flow import OmegaFPR302

# Setup the base database.
cruise_id = 'TEST_20230410D'
mdb = MARDB(cruise_id)

# Instantiate devices.
gps = AdafruitHAT(serial_number = '000001')
pump = ShurfloBaitmaster(serial_number="pump00001")
valve = AtlanticBVB4TV(serial_number="valve00002")
tsg = AtlasTSG(serial_number = '000001')
flowmeter = OmegaFPR302(serial_number = '11222239', kfactor = 617.5)

# Disable the pump and valve by default.
valve.tsw()
pump.off()

for i in range(20):
    t1 = time.monotonic()
    if i == 10:
        valve.fsw()
    #     pump.on()
    mdb.write_tsg(tsg.get_state())
    mdb.write_gps(gps.get_state())
    mdb.write_pump(pump.get_state())
    mdb.write_valve(valve.get_state())
    mdb.write_flow(flowmeter.get_state())
    t2 = time.monotonic()
    time.sleep(t2-t1)
    print(t2-t1)


# Turn off pump and valve.
valve.tsw()
pump.off()