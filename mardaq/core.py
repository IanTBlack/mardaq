import logging
import netrc
import os
import time
import yaml

def load_config(filepath):
    console_log = console_logger(1)
    try:
        with open(filepath, 'r') as stream:
            cfg = yaml.safe_load(stream)
            console_log.debug('Valid format config loaded.')
            return cfg
    except:
        console_log.critical('Invalid config format.')
        raise IOError

    # def load_config():
    # console_log = console_logger(2)
    # drives = os.listdir(f"/media/{os.getlogin()}/")
    # if len(drives) == 1:
    #     [drive] = drives
    #     cfg_path = f"/media/{os.getlogin()}/{drive}/config/deployment.cfg"
    #     with open(cfg_path, 'r') as stream:
    #         cfg = yaml.safe_load(stream)
    #         console_log.info('Valid format config loaded.')
    #         return cfg
    # elif len(drives) >= 2:
    #     raise NotImplementedError('Support for multiple data drives is not yet implemented.')
    # elif len(drives) == 0:
    #     raise NotADirectoryError('No external drive detected.')

def load_table_structure(filepath, structure_id):
    with open(filepath, 'r') as stream:
        tables = yaml.safe_load(stream)
    table_structure = tables[structure_id]
    fields = list(table_structure.keys())
    pg_dtypes = [v['pg_dtype'] for v in table_structure.values()]
    np_dtypes = [v['np_dtype'] for v in table_structure.values()]
    return (fields, pg_dtypes, np_dtypes)

def load_metadata(filepath, metadata_id):
    with open(filepath, 'r') as stream:
        md = yaml.safe_load(stream)
    smd = md[metadata_id]
    gmd = md['global']
    metadata = {**gmd, **smd}
    return metadata

def load_credentials(netrc_location):
    u, _, p = netrc.netrc(netrc_location).authenticators('mardaq')
    return u, p

def console_logger(console_level=2):
    logger = logging.getLogger('mardaq_console')
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


def file_logger():
    logger = logging.getLogger('mardaq_file')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        file = logging.FileHandler('mardaq_debug.log')
        file.setLevel(logging.DEBUG)
        dtfmt = '%Y-%m-%dT%H:%M:%S'
        strfmt = '%(asctime)s.%(msecs)03dZ | %(levelname)-8s | %(message)s'
        file_fmt = logging.Formatter(strfmt, datefmt=dtfmt)
        file_fmt.converter = time.gmtime
        file.setFormatter(file_fmt)
        logger.addHandler(file)
    if logger:
        return logger
    else:
        raise ReferenceError("Logger not found.")
