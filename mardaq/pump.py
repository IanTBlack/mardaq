from mardaq.core import *
from mardaq.relay import Relay

class ShurfloBaitmaster():
    def __init__(self, serial_number,channel = 1):
        self.sn = serial_number
        self.relay = Relay()
        if channel == 1:
            self.pin = self.relay.One
        elif channel == 2:
            self.pin = self.relay.Two
        elif channel == 3:
            self.pin = self.relay.Three

    def on(self):
        self.relay.enable(self.pin)

    def off(self):
        self.relay.disable(self.pin)

    def get_state(self):
        dt, relay_state = self.relay.state(self.pin)
        if relay_state is False:
            pump_on = False
        elif relay_state is True:
            pump_on = True
        return (self.sn, dt, relay_state, pump_on)


    def closeout(self) -> None:
        self.relay.deinitialize()

