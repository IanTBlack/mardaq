from datetime import datetime, timezone
import numpy as np
import os
import re
import time

from pyACS.acs import ACS as PY_ACS
from mardaq.interfaces.rs232 import RS232
from mardaq.core import console_logger

class ACS(PY_ACS):
    def __init__(self, input_device_filepath):
        self.console_log = console_logger()
        self._dev_file = os.path.normpath(input_device_filepath)
        super().__init__(os.path.abspath(self._dev_file))
        with open(self._dev_file , 'r') as devf:
            self._dev_lines = devf.readlines()
        self._get_offset_creation_date()
        self._get_tcal_ical()
        self._get_noise_conform()
        self.__sn = self.get_serial_number(self.serial_number)
        self.console_log.info(f"{self.__sn} initialized.")

    def __enter__(self):
        return self

    def __exit__(self,et,ev,etb):
        self.disconnect()


    def connect(self, com_port):
        self.rs232 = RS232()
        self.com_port = com_port
        if self.rs232.connect(self.com_port, baudrate = 115200) is True:
            self.console_log.debug(f'Connected to {self.__sn}')
            self.rs232.clear_buffers()
        else:
            self.console_log.critical(f'Unable to connect to {self.__sn}.')
            raise ConnectionError
        self._reset_frame_buffer()
        time.sleep(1)
        if self.rs232._serial.is_open and self.rs232._serial.in_waiting == 0:
            self.console_log.critical(f'Unable to connect to {self.__sn}.')
            raise ConnectionError

    def _reset_frame_buffer(self):
        self._buffer = bytearray()

    def _get_frame(self):
        valid_counter = 0
        while True:
            #timestamp = datetime.now(timezone.utc)
            timestamp = datetime.now()
            data = self.rs232.read_buffer()
            self._buffer.extend(data)
            bin_frame, valid, self._buffer, unknown_bytes = self.find_frame(self._buffer)
            if valid is None:
                valid_counter +=1
                if valid_counter == 10 and self._buffer == 0:
                    self.console_log.critical('Sensor is not sending data!')
                continue
            else:
                raw_frame = self.unpack_frame(bin_frame)
                cal_frame = self.calibrate_frame(raw_frame, get_external_temperature = True)
                return (timestamp,bin_frame, raw_frame, cal_frame)


    def power_flag(self, acs_timestamp):
        if acs_timestamp <= 240 * 1000:
            power_on_flag = 4
        else:
            power_on_flag = 1
        return power_on_flag

    def flag_temp_outside_cal_range(self, original_flag):
        if original_flag == 0:
            new_flag = 1
        elif original_flag == 1:
            new_flag = 4
        return new_flag


    def get_data(self):
        dt, bin_frame, raw_frame, cal_frame = self._get_frame()

        a_sig = list(raw_frame.a_sig)
        a_ref = list(raw_frame.a_ref)
        a_uncorr = list((1 / self.x) * np.log(np.array(a_sig) / np.array(a_ref)))

        c_sig = list(raw_frame.c_sig)
        c_ref = list(raw_frame.c_ref)
        c_uncorr = list((1 / self.x) * np.log(np.array(c_sig) / np.array(c_ref)))

        internal_temperature = float(cal_frame.internal_temperature)
        dta, dtc = self.f_delta_t_a(internal_temperature),self.f_delta_t_c(internal_temperature)

        fields_data = {'serial_number': self.__sn,
                       'time': dt,
                       'dev_file': self._dev_file,
                       'frame_type': int(raw_frame.frame_type),
                       'frame_length': int(raw_frame.frame_len),
                       'output_wavelengths': int(raw_frame.output_wavelength),
                       'raw_binary_frame': bin_frame,
                       'raw_internal_temperature': int(raw_frame.t_int),
                       'raw_external_temperature': int(raw_frame.t_ext),
                       'internal_temperature': internal_temperature,
                       'external_temperature': float(cal_frame.external_temperature),
                       'pressure_counts': int(raw_frame.p),
                       'wavelength_a': list(self.lambda_a),
                       'a_ref_dark': int(raw_frame.a_ref_dark),
                       'a_sig_dark': int(raw_frame.a_sig_dark),
                       'a_sig': a_sig,
                       'a_ref': a_ref,
                       'a_offsets': list(self.offset_a),
                       'a_uncorr': a_uncorr,
                       'delta_t_a': list(dta),
                       'a_m': list(cal_frame.a),
                       'wavelength_c': list(self.lambda_c),
                       'c_ref_dark': int(raw_frame.c_ref_dark),
                       'c_sig_dark': int(raw_frame.c_sig_dark),
                       'c_sig': c_sig,
                       'c_ref': c_ref,
                       'c_offsets': list(self.offset_c),
                       'c_uncorr': c_uncorr,
                       'delta_t_c': list(dtc),
                       'c_m': list(cal_frame.c),
                       'time_since_power': int(raw_frame.time_stamp),
                       'flag_time_since_power': self.power_flag(int(raw_frame.time_stamp)),
                       'flag_temp_outside_cal_range': self.flag_temp_outside_cal_range(cal_frame.flag_outside_calibration_range)}
        return fields_data



    def get_serial_number(self, bin_sn):
        int_sn = int(bin_sn[-6:], 16)
        str_sn = 'ACS' + str.zfill(str(int_sn),3)
        return str_sn


    def _get_offset_creation_date(self):
        [loi] = [_line for _line in self._dev_lines if 'The offsets were saved' in _line]  # Get line of interest.
        loi = loi.replace(' ', '')
        self._dev_created_date = datetime.strptime(re.findall('on(.*?)\.', loi)[0], '%m/%d/%Y')


    def _get_tcal_ical(self):
        [loi] = [_line for _line in self._dev_lines if 'tcal:' in _line and 'ical:' in _line]  # Get line of interest.
        self.tcal, self.ical = [float(v) for v in re.findall('tcal:(.*?)C, ical:(.*?) C', loi)[0]]


    def _get_noise_conform(self):
        [loi] = [_line for _line in self._dev_lines if 'maxANoise' in _line]  # Get line of interest.
        values, params = loi.split(';')
        values = [float(v) for v in values.split('\t') if v != '']
        params = [str(v) for v in params.split('\t') if v != '']
        params = [p.replace(' ', '') for p in params]
        params = [p.replace('\n', '') for p in params]
        _dict = dict(zip(params, values))
        for k, v in _dict.items():
            setattr(self, k, v)

    def disconnect(self):
        self.rs232.disconnect()