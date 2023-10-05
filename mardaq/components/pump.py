from mardaq.components.relay import Relay
class SHURFLOBAITMASTER():
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

    def get_data(self):
        dt, relay_state = self.relay.state(self.pin)
        if relay_state is False:
            pump_on = 0
        elif relay_state is True:
            pump_on = 1
        relay_state = int(relay_state)
        fields_data = {'serial_number': self.sn,
                       'time': dt,
                       'pump_relay_state': relay_state,
                       'pump_on': pump_on}
        return fields_data


    def closeout(self) -> None:
        self.relay.deinitialize()
