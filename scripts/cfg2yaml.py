import yaml

def cfg2yaml(CFG):


cfg = {'deployment': None,
       'system_sn': 'flowthrough_sel',
       'mode': 'auto',
       'pump':{'enabled': True,
               'sn': 'pump'}}



class CFG:
    DEPLOYMENT = None
    SYSTEM = None
    MODE = 'auto'

    class PUMP:
        ENABLED = True
        SN = 'pump00001'
        MODEL = 'SHURFLO BAITMASTER'
        RELAY = 1

    class VALVE:
        ENABLED = True
        SN = 'valve00001'
        MODEL = 'ATLANTIC'
        RELAY = 2

    class POWER_RELAY_12V:
        ENABLED = True
        RELAY = 3

    class GPS:
        ENABLED = True
        SN = 'gps00001'
        MODEL = 'ADAFRUIT GPS HAT'
        SERIAL_PORT = '/dev/ttyS0'

    class INTAKE_THERMISTOR:
        ENABLED = True
        SN = 'therm00001'
        MODEL = 'ATLAS PT1000'
        I2C_ADDRESS = 0x77

    class TSG:
        ENABLED = True
        SN = 'tsg00001'
        MODEL = 'ATLAS K1.0 Industrial'
        I2C_ADDRESS_THERM = 0x76
        I2C_ADDRESS_EC = 0x67

    class ACS:
        ENABLED = True
        SN = 'acs011'
        MODEL = 'WETLabs ACS'
        SERIAL_PORT = '/dev/ttyUSB0'


