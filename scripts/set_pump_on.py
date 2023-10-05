#!/usr/bin/python

from mardaq.core import load_config
from mardaq.components.pump import SHURFLOBAITMASTER

def main():
    cfg = load_config('/home/sel/mardaq/config/deployment.cfg')
    scfg = cfg['sensors']['pump1']
    pump = SHURFLOBAITMASTER(scfg['sn'])
    pump.on()

if __name__ == "__main__":
    main()