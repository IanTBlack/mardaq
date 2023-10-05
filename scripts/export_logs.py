
import os
import shutil

def main():
    local_filepath = '/home/sel/mardaq/logs/cron.log'
    ext_drives = os.listdir(f'/media/{os.getlogin()}')
    if len(ext_drives) == 0:
        exit(0)
    elif len(ext_drives) == 1:
        [drive] = ext_drives
    drive_path = f'/media/{os.getlogin()}/{drive}'
    ext_data_path = f"{drive_path}/logs"
    os.makedirs(ext_data_path, exist_ok=True)
    ext_filepath = f"{ext_data_path}/cron.log"
    shutil.copy(local_filepath, ext_filepath)

if __name__ == "__main__":
    main()