import time
from mardaq.core import load_config
from mardaq.components.valve import ATLANTICBVB4TV


def main():
    cfg = load_config()
    if cfg['sensors']['valve1']['enabled'] is False:
        pass
    else:
        valve1 = ATLANTICBVB4TV(cfg['sensors']['valve1']['sn'], channel = cfg['sensors']['valve1']['relay_channel'])
    valve1.tsw()
    init_time = time.monotonic()
    while True:
        check_time = time.monotonic()
        if check_time - init_time >= cfg['filter_every']:
            valve1.fsw()
            time.sleep(cfg['filter_for'])
            valve1.tsw()
            init_time = time.monotonic()
        else:
            time.sleep(1)


if __name__ == "__main__":
    main()