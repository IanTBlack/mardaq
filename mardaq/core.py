import logging
import os
import time
import yaml


def load_config():
    _logger = initialize_logger()
    drives = os.listdir(f"/media/{os.getlogin()}/")
    if len(drives) == 1:
        [drive] = drives
        cfg_path = f"/media/{os.getlogin()}/{drive}/config/mardaq.cfg"
        with open(cfg_path, 'r') as stream:
            cfg = yaml.safe_load(stream)
            _logger.info('Valid format config loaded.')
            return cfg
    elif len(drives) >= 2:
        raise NotImplementedError('Support for multiple data drives is not yet implemented.')
    elif len(drives) == 0:
        raise NotADirectoryError('No external drive detected.')


def initialize_logger(console_level=2):
    logger = logging.getLogger('mardaq')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        console = logging.StreamHandler()
        if console_level == 0:
            console.setLevel(logging.ERROR)
        elif console_level == 1:
            console.setLevel(logging.INFO)
        elif console_level == 2:
            console.setLevel(logging.DEBUG)
        else:
            raise ValueError("Console level must be an int between 0-2.")
        dtfmt = '%Y-%m-%dT%H:%M:%S'
        strfmt = '%(asctime)s.%(msecs)03dZ | %(levelname)-8s | %(message)s'
        console_fmt = logging.Formatter(strfmt, datefmt=dtfmt)
        console_fmt.converter = time.gmtime
        console.setFormatter(console_fmt)
        logger.addHandler(console)
    if logger:
        return logger
    else:
        raise ReferenceError("Logger not found.")