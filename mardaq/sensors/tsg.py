from datetime import datetime, timezone
import gsw
import time
import numpy as np

from mardaq.sensors.ezo import EZO
from mardaq.core import console_logger

class ATLASTSG():
    def __init__(self, serial_number):
        self.console_log = console_logger(1)
        self.sn = serial_number
        self.ec = AtlasEC()
        self.rtd = AtlasRTD()
        self.console_log.info('TSG initialized.')

    def request_data(self):
        self.ec.ezo.send_cmd('R')
        self.rtd.ezo.send_cmd('R')

    def get_data(self):
        #dt = datetime.now(timezone.utc)
        dt = datetime.now()
        try:
            t = self.rtd.read_data()
            time.sleep(0.1)
            ec = self.ec.read_data()
            ec = ec * (1/1000)
            sp = float(gsw.SP_from_C(ec, t, p = 0))
            if sp < 2 or sp > 42: sp = np.nan
            self.console_log.debug('Data collected!')
        except:
            t = np.nan
            ec = np.nan
            sp = np.nan
            self.console_log.error('Error reading data from EC or RTD EZO.')

        fields_data = {'serial_number': self.sn,
                       'time': dt,
                       'temperature': t,
                       'conductivity': ec,
                       'practical_salinity': sp}
        return fields_data

    def get_data_compensated(self):
        try:
            t = self.rtd.take_sample()
            # dt = datetime.now(timezone.utc)
            dt = datetime.now()
            ec = self.ec.take_compensated_sample(t)
            ec = ec * (1/1000) # convert uS to ms
            sp = float(gsw.SP_from_C(ec, t, p = 0))
            # if sp < 2 or sp > 42: sp = np.nan
        except:
            dt = datetime.now()
            t = np.nan
            ec = np.nan
            sp = np.nan
            self.console_log.error('Error reading data from EC or RTD EZO.')

        fields_data = {'serial_number': self.sn,
                       'time': dt,
                       'temperature': t,
                       'conductivity': ec,
                       'practical_salinity': sp}
        return fields_data


class AtlasRTD():
    def __init__(self):
        self.console_log = console_logger(2)
        self.ezo = EZO(0x66)
        self.set_units()
        self.disable_chip_logger()
        self.console_log.debug('Setup Atlas RTD EZO.')

    def set_units(self):
        self.ezo.send_cmd('S,c')
        time.sleep(0.3)
        response = int.from_bytes(self.ezo.read_response(1),'big')
        if response == 1:
            self.console_log.debug('Set Atlas RTD units to Celsius.')
            return True
        else:
            self.console_log.error('Failure to set RTD units.')
            return False

    def disable_chip_logger(self):
        self.ezo.send_cmd('D,0')
        self.console_log.debug('Atlas RTD chip logger disabled.')
        time.sleep(0.3)

    def take_sample(self, wait = 0.6):
        self.ezo.send_cmd('R')
        time.sleep(wait)
        response = self.ezo.read_response()
        response = response.replace(b'\x00',b'')
        response = response.replace(b'\x01',b'')
        response = float(response)
        self.console_log.debug('Atlas RTD sample collected.')
        return response


    def read_data(self):
        response = self.ezo.read_response()
        response = response.replace(b'\x00',b'')
        response = response.replace(b'\x01',b'')
        response = float(response)
        return response

class AtlasEC():
    def __init__(self):
        self.console_log = console_logger(2)
        self.ezo = EZO(0x64)
        self.set_probe_type()
        self.disable_output(tds = True, salinity = True, specific_gravity=True)
        self.console_log.debug('Setup Atlas EC EZO.')

    def set_probe_type(self):
        self.ezo.send_cmd('K,1')
        time.sleep(0.3)
        response = int.from_bytes(self.ezo.read_response(1),'big')
        if response == 1:
            self.console_log.debug('Atlas EC probe type set to K 1.0.')
            return True
        else:
            self.console_log.error('Failure to set Atlas EC probe type.')
            return False

    def disable_output(self,tds=True,salinity = True,specific_gravity=True):
        cmd = 'O,'
        if tds is True:
            cmd = cmd + 'TDS,'
        if salinity is True:
            cmd = cmd + 'S,'
        if specific_gravity is True:
            cmd = cmd + 'SG,'
        cmd = cmd + '0'
        self.ezo.send_cmd(cmd)
        self.console_log.debug('Disabled TDS, Salinity, and SG output on Atlas EC EZO.')

    def take_sample(self,wait = 0.6):
        self.ezo.send_cmd('R')
        time.sleep(wait)
        response = self.ezo.read_response()
        response = response.replace(b'\x00',b'')
        response = response.replace(b'\x01',b'')
        response = float(response)
        self.console_log.debug('Atlas EC sample collected.')
        return response

    def read_data(self):
        response = self.ezo.read_response()
        response = response.replace(b'\x00',b'')
        response = response.replace(b'\x01',b'')
        response = float(response)
        return response

    def take_compensated_sample(self,temperature,wait = 0.6):
        cmd = f'RT,{temperature}'
        self.ezo.send_cmd(cmd)
        time.sleep(wait)
        response = self.ezo.read_response()
        response = response.replace(b'\x00',b'')
        response = response.replace(b'\x01',b'')
        response = float(response)
        self.console_log.debug('Atlas EC temperature compensated sample collected.')
        return response