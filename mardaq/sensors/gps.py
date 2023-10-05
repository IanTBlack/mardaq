from datetime import datetime, timezone
import numpy as np
from pynmeagps import NMEAReader
from serial import Serial
import time

from mardaq.core import console_logger


class ADAFRUITGPSHAT():
    def __init__(self, serial_number, port = '/dev/ttyS0', baudrate = 9600, timeout = 10):
        self.sn = serial_number
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.console_log = console_logger(1)
        self.establish_stream()
        self.console_log.info(f'GPS {self.sn} initialized on {self.port} at {self.baudrate} bps.')
        fields_data = self.get_data()
        if fields_data['gps_status'] == 'void':
            self.console_log.error('GPS signal is void.')


    def establish_stream(self):
        self.stream = Serial(self.port, baudrate = self.baudrate, timeout = self.timeout)
        self.nmr = NMEAReader(self.stream)


    def get_active_message(self):
        t1 = time.monotonic()
        while True:
            raw, parsed = self.nmr.read()
            if parsed.msgID == 'RMC':
                if parsed.status == 'A':
                    self.console_log.info('Active GPS signal acquired.')
                    break
            if time.monotonic() - t1 > 30:
                self.console_log.debug('Failure to acquire GPS for 30 seconds')
                return None, None
        return raw, parsed


    def get_data(self):
        #sysdt = datetime.now(timezone.utc)
        sysdt = datetime.now()
        while True:
            raw, parsed = self.nmr.read()
            if parsed.msgID == 'RMC':
                break
        gpsdt = datetime.combine(parsed.date, parsed.time)
        if parsed.status == 'A':
            self.console_log.debug('Active GPS signal acquired.')
            status = 'active'
            lon = parsed.lon
            lat = parsed.lat
        elif parsed.status == 'V':
            self.console_log.debug('GPS signal is void.')
            status = 'void'
            lon = np.nan
            lat = np.nan
        else:
            self.console_log.error('Unknown GPS condition.')
            status = parsed.status
            lon = parsed.lon
            lat = parsed.lat
        fields_data = {'serial_number': self.sn,
                       'time': sysdt,
                       'gps_time': gpsdt,
                       'latitude': lat,
                       'longitude': lon,
                       'cog': parsed.cog,
                       'sog': parsed.spd,
                       'gps_status': status,
                       'nmea_message': raw.decode()}
        return fields_data
