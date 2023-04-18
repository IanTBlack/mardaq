from mardaq.core import *
from mardaq.gps import AdafruitHAT

def main():
    gps = AdafruitHAT('00001')
    raw, parsed = gps.get_active_message()

    if parsed is not None:
        disable_ntp()
        gps_time = datetime.combine(parsed.date, parsed.time)
        manual_time = gps_time.strftime('%Y-%m-%d %H:%M:%S')
        cmd = f"sudo date -s '{manual_time}'"
        os.system(cmd)
    elif parsed is None:
        msg = "GPS was unable to acquire a stable datetime. Continuing with NTP time."
        raise UserWarning(msg)

if __name__ == "__main__":
    main()