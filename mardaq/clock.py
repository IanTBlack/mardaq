from datetime import datetime
import os
from mardaq.sensors.gps import ADAFRUITGPSHAT


def disable_ntp():
    """Disables NTP functionality so the clock can be set by a non-networked time source."""
    cmd = 'sudo timedatectl set-ntp false'
    os.system(cmd)


def enable_ntp():
    """Enables NTP functionality so the network clock can be the time source."""
    cmd = 'sudo timedatectl set-ntp true'
    os.system(cmd)


def set_clock_with_gps(gps):
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

def set_clock_source(method = 'ntp'):
    if method == 'ntp':
        enable_ntp()
    elif method == 'gps':
        set_clock_with_gps(ADAFRUITGPSHAT('placeholder'))
    


