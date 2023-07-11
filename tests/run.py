import multiprocessing
import subprocess

def main():
    scripts = ['/home/sel/mardaq/scripts/record_gps.py',
               '/home/sel/mardaq/scripts/record_tsg.py']
               # 'scripts/record_valve.py',
               # 'scripts/record_acs.py',
               # 'scripts/record_pump.py',
               # 'scripts/drive_pump.py',
               # 'scripts/record_flow.py',
               # 'scripts/drive_valve.py']

    count = len(scripts)
    pool = multiprocessing.Pool(processes = count)
    pool.map(work, scripts)

def work(script):
    return subprocess.call(['python', script])

if __name__ == '__main__':
    main()