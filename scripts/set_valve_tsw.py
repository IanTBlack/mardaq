#!/usr/bin/python

from mardaq.core import load_config, console_logger
from mardaq.components.valve import ATLANTICBVB4TV

def main():
    console_log = console_logger(1)
    cfg = load_config('/home/sel/mardaq/config/deployment.cfg')
    scfg = cfg['sensors']['valve1']
    valve = ATLANTICBVB4TV(scfg['sn'])
    valve.tsw()
    console_log.info('Valve set to TSW.')
if __name__ == "__main__":
    main()