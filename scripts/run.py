import multiprocessing
import subprocess

from mardaq.core import console_logger

def main():
    console_log = console_logger(1)
    console_log.info('Setting up data storage drive...')
    output = subprocess.call(['python','/home/sel/mardaq/scripts/setup_extra_drive.py'])
    if output == 0:
        console_log.info('Data storage drive configured.')
    else:
        console_log.warning('External storage drive not found.')
    filepaths = ['/home/sel/mardaq/scripts/record_pump1.py',
                 '/home/sel/mardaq/scripts/record_gps1.py',
                 '/home/sel/mardaq/scripts/record_flow1.py',
                 '/home/sel/mardaq/scripts/record_valve1.py',
                 '/home/sel/mardaq/scripts/record_tsg1.py',
                 '/home/sel/mardaq/scripts/record_acs1.py']
    pool = multiprocessing.Pool(processes = len(filepaths))
    pool.map(subprocess.call,[['python',script] for script in filepaths])

if __name__ == "__main__":
    main()