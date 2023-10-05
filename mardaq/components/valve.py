from mardaq.components.relay import Relay
from mardaq.core import console_logger
class ATLANTICBVB4TV():
    def __init__(self, serial_number, channel = 2):
        self.console_log = console_logger(1)
        self.sn = serial_number
        self.relay = Relay()
        if channel == 1:
            self.pin = self.relay.One
        elif channel == 2:
            self.pin = self.relay.Two
        elif channel == 3:
            self.pin = self.relay.Three
        self.console_log.info(f'Valve initialized on channel {channel}.')

    def fsw(self):
        self.relay.enable(self.pin)

    def tsw(self):
        self.relay.disable(self.pin)


    def get_data(self):
        dt, relay_state = self.relay.state(self.pin)
        if relay_state is False:
            seawater_state = 0 #TSW
        elif relay_state is True:
            seawater_state = 1 #FSW
        relay_state = int(relay_state)

        fields_data = {'serial_number': self.sn,
                       'time': dt,
                       'valve_relay_state': relay_state,
                       'seawater_state': seawater_state}

        return fields_data


    def closeout(self) -> None:
        self.relay.deinitialize()
