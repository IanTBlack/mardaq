from mardaq.core import *

class AdafruitHAT():
    def __init__(self, serial_number, port = '/dev/ttyS0', baudrate = 9600, timeout = 10):
        self.sn = serial_number
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.establish_stream()

    def establish_stream(self):
        self.stream = Serial(self.port, baudrate = self.baudrate, timeout = self.timeout)
        self.nmr = NMEAReader(self.stream)

    def get_active_message(self):
        t1 = time.monotonic()
        while True:
            raw, parsed = self.nmr.read()
            if parsed.msgID == 'RMC':
                if parsed.status == 'A':
                    break
            if time.monotonic() - t1 > 30:
                return None, None
        return raw, parsed

    def get_state(self):
        sysdt = datetime.now(timezone.utc)
        while True:
            raw, parsed = self.nmr.read()
            if parsed.msgID == 'RMC':
                break
        gpsdt = datetime.combine(parsed.date, parsed.time)
        if parsed.status == 'A':
            status = 'active'
        elif parsed.status == 'V':
            status = 'void'
        else:
            status = parsed.status
        return (self.sn, sysdt, raw, status, gpsdt, parsed.lat, parsed.lon, parsed.cog, parsed.spd)
