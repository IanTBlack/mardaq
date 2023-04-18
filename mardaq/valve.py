from mardaq.core import *
from mardaq.relay import Relay


class AtlanticBVB4TV():
    def __init__(self, serial_number, channel = 2):
        self.sn = serial_number
        self.relay = Relay()
        if channel == 1:
            self.pin = self.relay.One
        elif channel == 2:
            self.pin = self.relay.Two
        elif channel == 3:
            self.pin = self.relay.Three


    def fsw(self):
        self.relay.enable(self.pin)

    def tsw(self):
        self.relay.disable(self.pin)


    def get_state(self):
        dt, relay_state = self.relay.state(self.pin)
        if relay_state is False:
            seawater_state = "TSW"
        elif relay_state is True:
            seawater_state = "FSW"
        return (self.sn, dt, relay_state, seawater_state)


    def closeout(self) -> None:
        self.relay.deinitialize()
