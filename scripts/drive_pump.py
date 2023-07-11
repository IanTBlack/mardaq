import time
from mardaq.core import load_config
from mardaq.components.pump import SHURFLOBAITMASTER


def main():
    cfg = load_config()
    if cfg['sensors']['pump']['enabled'] is False:
        pass
    else:
        pump = SHURFLOBAITMASTER(cfg['sensors']['pump']['sn'], channel = cfg['sensors']['pump']['relay_channel'])
        time.sleep(3)
        pump.on()

if __name__ == "__main__":
    main()