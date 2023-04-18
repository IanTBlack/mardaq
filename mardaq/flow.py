from mardaq.core import *


class OmegaFPR302():
    def __init__(self, serial_number, kfactor, CIO_pin = 18):
        self.sn = serial_number
        self.kfac = kfactor
        self.handle = ljm.openS("T7","ANY", "ANY")
        self.identify_pin(CIO_pin)
        self.get_info()
        try:
            self.reset_counter()
            self.disable_clock()
            self.setup_pins()
        except:
            self.setup_pins()
        self.old_sample = None


    def get_info(self):
        self.device_type, self.connection_type, self.t7_sn, self.ip_address, self.port, self.max_bytes = ljm.getHandleInfo(self.handle)

    def __enter__(self):
        return self

    def __exit__(self, et, ev, etb):
        self.closeout()

    def closeout(self):
        ljm.close(self.handle)

    def identify_pin(self,pin):
        if pin == 16 or pin == 'CIO0':
            self._pin = 16
        elif pin == 17 or pin == 'CIO1':
            self._pin = 17
        elif pin == 18 or pin == 'CIO2':
            self._pin = 18
        elif pin == 19 or pin == 'CIO3':
            self._pin = 19

    def setup_pins(self):
        pin_settings = {'DIO_EF_CLOCK0_DIVISOR': 1,
                        'DIO_EF_CLOCK0_ROLL_VALUE': 400000,
                        'DIO_EF_CLOCK0_ENABLE': 1,
                        f"DIO{self._pin}_EF_INDEX": 7,
                        f"DIO{self._pin}_EF_ENABLE": 1}
        names = list(pin_settings.keys())
        values = list(pin_settings.values())
        num_frames = len(pin_settings)
        try:
            results = ljm.eWriteNames(self.handle,num_frames, names, values)
        except:
            pass

    def reset_counter(self):
        results = ljm.eReadName(self.handle, f'DIO{self._pin}_EF_READ_A_AND_RESET')

    def disable_clock(self):
        pin_settings = {"DIO_EF_CLOCK0_ENABLE" : 0}
        names = list(pin_settings.keys())
        values = list(pin_settings.values())
        num_frames = len(pin_settings)
        results = ljm.eWriteNames(self.handle, num_frames, names, values)

    def get_pulses(self):
        pulses = ljm.eReadName(self.handle, f"DIO{self._pin}_EF_READ_A")
        return pulses

    def get_state(self):
        dt = datetime.now(timezone.utc)
        pulses = self.get_pulses()
        gal = pulses/self.kfac
        ml = round(gal * 3785.41,2)
        if self.old_sample is None:
            ml_per_min = 0
        elif self.old_sample is not None:
            last_ml = self.old_sample[4]
            last_dt = self.old_sample[1]
            delta_dt = dt - last_dt
            delta_ml = ml - last_ml
            ml_per_min = (delta_ml / delta_dt.total_seconds()) * 60
        data_tuple = (self.sn, dt, self.kfac, pulses, ml, ml_per_min)
        self.old_sample = data_tuple
        return data_tuple
