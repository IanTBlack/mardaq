# import board
# import busio
from datetime import datetime, timedelta, timezone
import fcntl
import io
# from labjack import ljm
import logging
from netrc import netrc
import mysql.connector
# from netCDF4 import Dataset
import pandas as pd
import numpy as np
import os
from pynmeagps import NMEAReader
import RPi.GPIO as GPIO
from serial import Serial
import subprocess
import smbus
import sys
import time
import yaml


# DEFAULT GLOBAL ENVIRONMENTAL VARIABLES
os.environ['MARDAQ_PUMP_MODE'] = 'MANUAL'
os.environ['MARDAQ_VALVE_MODE'] = 'MANUAL'

USER = os.getlogin()
MEDIA_DIR = os.path.normpath(f"/media/{USER}")
DRIVE_DIR = os.path.join(MEDIA_DIR, "flowthrough")
DATA_DIR = os.path.join(DRIVE_DIR, "data")
CONFIG_DIR = os.path.join(DRIVE_DIR, "config")
SPRF_DIR = os.path.join(CONFIG_DIR,"sensor_profiles")
ACTIVE_CFG = os.path.join(CONFIG_DIR,'active.cfg')

NETRC_LOC = os.path.join(f"/home/{USER}/.netrc")


def read_config():
    with open(ACTIVE_CFG, 'r') as cfg_file:
        cfg = yaml.safe_load(cfg_file)
    return cfg


def setup_gps():
    stream = Serial('/dev/serial0',9600, timeout=10)
    nmr = NMEAReader(stream)
    return nmr


def disable_ntp():
    """Disables NTP functionality so the clock can be set by a non-networked time source."""
    cmd = 'sudo timedatectl set-ntp false'
    os.system(cmd)


def enable_ntp():
    """Enables NTP functionality so the network clock can be the time source."""
    cmd = 'sudo timedatectl set-ntp true'
    os.system(cmd)