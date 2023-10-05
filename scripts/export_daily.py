import subprocess
import time

from mardaq.core import console_logger

def main():
    console_log = console_logger(1)
    t1 = time.monotonic()
    output = subprocess.call(['python', '/home/sel/mardaq/scripts/setup_extra_drive.py'])
    if output != 0:
        raise NotADirectoryError
    filepaths = ['/home/sel/mardaq/scripts/export_pump1.py',
                 '/home/sel/mardaq/scripts/export_acs1.py',
                 '/home/sel/mardaq/scripts/export_tsg1.py',
                 '/home/sel/mardaq/scripts/export_gps1.py',
                 '/home/sel/mardaq/scripts/export_flow1.py',
                 '/home/sel/mardaq/scripts/export_valve1.py',
                 '/home/sel/mardaq/scripts/export_logs.py']

    for filepath in filepaths:
        subprocess.call(['python', filepath])
    t2 = time.monotonic()
    console_log.info(f'Time to export data: {round(t2-t1,2)} seconds.')

if __name__ == "__main__":
    main()