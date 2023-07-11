from datetime import datetime, timezone
import numpy as np
from pynmeagps import NMEAReader
from serial import Serial
import time

from mardaq.core import initialize_logger

class ADAFRUITGPSHAT():
    def __init__(self, serial_number, port = '/dev/ttyS0', baudrate = 9600, timeout = 10):
        self.sn = serial_number
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._logger = initialize_logger()
        self.establish_stream()



    def establish_stream(self):
        self.stream = Serial(self.port, baudrate = self.baudrate, timeout = self.timeout)
        self.nmr = NMEAReader(self.stream)
        self._logger.info(f'GPS {self.sn} setup on {self.port} at {self.baudrate} bps.')


    def get_active_message(self):
        t1 = time.monotonic()
        while True:
            raw, parsed = self.nmr.read()
            if parsed.msgID == 'RMC':
                if parsed.status == 'A':
                    self._logger.info('Active GPS signal acquired.')
                    break
            if time.monotonic() - t1 > 30:
                self._logger.debug('Failure to acquire GPS for 30 seconds')
                return None, None
        return raw, parsed


    def get_data(self):
        sysdt = datetime.now(timezone.utc)
        while True:
            raw, parsed = self.nmr.read()
            if parsed.msgID == 'RMC':
                break
        gpsdt = datetime.combine(parsed.date, parsed.time)
        if parsed.status == 'A':
            self._logger.info('Active GPS signal acquired.')
            status = 'active'
            lon = parsed.lon
            lat = parsed.lat
        elif parsed.status == 'V':
            self._logger.debug('GPS signal is void.')
            status = 'void'
            lon = np.nan
            lat = np.nan
        else:
            status = parsed.status
            lon = parsed.lon
            lat = parsed.lat
        return (sysdt, lat, lon, parsed.cog, parsed.spd, gpsdt, status, raw, self.sn)
