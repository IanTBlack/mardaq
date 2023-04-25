import gsw

from mardaq.core import *
from mardaq.ezo import EZO


class AtlasTSG():
    def __init__(self,serial_number):
        self.sn = serial_number
        self.ec = AtlasEC()
        self.rtd = AtlasRTD()
        self.standard_temp = 25
        self.a = 0.0187 # Hayashi, 2003


    def get_state(self):
        self.ec.ezo.send_cmd('R')
        self.rtd.ezo.send_cmd('R')
        time.sleep(0.6)
        t = self.rtd.ezo.read_response()
        t = t.replace(b'\x00',b'')
        t = t.replace(b'\x01',b'')
        t = float(t)
        ec = self.ec.ezo.read_response()
        ec = ec.replace(b'\x00',b'')
        ec = ec.replace(b'\x01',b'')
        ec = float(ec) * (1/1000) # convert uS to ms

        # c = self.a/(1+(self.a * (self.standard_temp - 25)))  #Hayashi, 2003
        # comp_ec = ec * (1 - (c * (t - self.standard_temp)))

        # pracsal = float(gsw.SP_from_C(ec, t, p = 0))


        dt = datetime.now(timezone.utc) - timedelta(milliseconds=300)
        return (self.sn, dt, t, ec)


    # def get_compensated_state(self):
    #     t = self.rtd.take_sample()
    #     ec = self.ec.take_compensated_sample(t)
    #     dt = datetime.now(timezone.utc) - timedelta(milliseconds=300)
    #     return (self.sn, dt,t,ec)


class AtlasRTD():
    def __init__(self):
        self.ezo = EZO(0x66)
        self.set_units()
        self.disable_chip_logger()

    def set_units(self):
        self.ezo.send_cmd('S,c')
        time.sleep(0.3)
        response = int.from_bytes(self.ezo.read_response(1),'big')
        if response == 1:
            return True
        else:
            return False

    def disable_chip_logger(self):
        self.ezo.send_cmd('D,0')
        time.sleep(0.3)

    def take_sample(self,wait = 0.6):
        self.ezo.send_cmd('R')
        time.sleep(wait)
        response = self.ezo.read_response()
        response = response.replace(b'\x00',b'')
        response = response.replace(b'\x01',b'')
        response = float(response)
        return response


class AtlasEC():
    def __init__(self):
        self.ezo = EZO(0x64)
        self.set_probe_type()
        self.disable(tds = True, salinity = True, specific_gravity=True)

    def set_probe_type(self):
        self.ezo.send_cmd('K,1')
        time.sleep(0.3)
        response = int.from_bytes(self.ezo.read_response(1),'big')
        if response == 1:
            return True
        else:
            return False

    def disable(self,tds=True,salinity = True,specific_gravity=True):
        cmd = 'O,'
        if tds is True:
            cmd = cmd + 'TDS,'
        if salinity is True:
            cmd = cmd + 'S,'
        if specific_gravity is True:
            cmd = cmd + 'SG,'
        cmd = cmd + '0'
        self.ezo.send_cmd(cmd)


    def take_sample(self,wait = 0.6):
        self.ezo.send_cmd('R')
        time.sleep(wait)
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
        return response