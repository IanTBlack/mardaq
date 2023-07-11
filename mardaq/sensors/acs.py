from datetime import datetime, timezone
import os

from pyACS.acs import ACS as PY_ACS
import re
from mardaq.interfaces.rs232 import RS232

class ACS(PY_ACS):
    def __init__(self, serial_number, input_device_filepath):
        super().__init__(os.path.abspath(input_device_filepath))
        self._dev_file = input_device_filepath
        self._real_sn = serial_number
        self._cal_file = os.path.basename(os.path.normpath(self._dev_file))

        with open(input_device_filepath, 'r') as dev_file:
            self._dev_lines = dev_file.readlines()
        self._get_offset_creation_date()
        self._get_tcal_ical()
        self._get_noise_conform()

    def connect(self, com_port):
        self.rs232 = RS232()
        self.com_port = com_port
        if self.rs232.connect(self.com_port, baudrate = 115200) is True:
            self.rs232.clear_buffers()
        self._reset_frame_buffer()

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

    def _reset_frame_buffer(self):
        self._buffer = bytearray()

    def _get_frame(self):
        timestamp = datetime.now(timezone.utc)
        valid_counter = 0
        while True:
            data = self.rs232.read_buffer()
            self._buffer.extend(data)
            frame, valid, self._buffer, unknown_bytes = self.find_frame(self._buffer)
            if valid is None:
                valid_counter +=1
                if valid_counter == 10 and self._buffer == 0:
                    raise ConnectionError('Sensor is not sending data!')
                continue
            else:
                raw_frame = self.unpack_frame(frame)
                cal_frame = self.calibrate_frame(raw_frame, get_external_temperature = True)
                return (timestamp, raw_frame, cal_frame)

    def get_data(self):
        dt, raw, cal = self._get_frame()
        a_ref = str(list(raw.a_ref))
        c_ref = str(list(raw.c_ref))
        a_sig = str(list(raw.a_sig))
        c_sig = str(list(raw.c_sig))
        a = str(list(cal.a))
        c = str(list(cal.c))

        a_wvls = str(list(self.lambda_a))
        c_wvls = str(list(self.lambda_c))

        data = (dt,
                a,
                c,
                a_wvls,
                c_wvls,
                cal.internal_temperature,
                cal.external_temperature,
                cal.flag_outside_calibration_range,
                raw.output_wavelength,
                raw.time_stamp,
                raw.t_int,
                raw.t_ext,
                raw.p,
                raw.frame_len,
                raw.frame_type,
                raw.a_ref_dark,
                raw.a_sig_dark,
                raw.c_ref_dark,
                raw.c_sig_dark,
                a_ref,
                a_sig,
                c_ref,
                c_sig,
                self._cal_file,
                self._real_sn)

        return data


    def get_data4nc(self):
        dt, raw, cal = self._get_frame()
        a_ref = raw.a_ref
        c_ref = raw.c_ref
        a_sig = raw.a_sig
        c_sig = raw.c_sig
        a = cal.a
        c = cal.c

        a_wvls = self.lambda_a
        c_wvls = self.lambda_c

        data = {'time': dt,
                'a': a,
                'c': c,
                'a_wavelength': a_wvls,
                'c_wavelength': c_wvls,
                'internal_temperature': cal.internal_temperature,
                'external_temperature': cal.external_temperature,
                'outside_cal_flag': cal.flag_outside_calibration_range,
                'output_wavelengths': raw.output_wavelength,
                'power_on': raw.time_stamp,
                't_int': raw.t_int,
                't_ext': raw.t_ext,
                'pressure_counts': raw.p,
                'frame_len': raw.frame_len,
                'frame_type': raw.frame_type,
                'a_ref_dark': raw.a_ref_dark,
                'a_sig_dark': raw.a_sig_dark,
                'c_ref_dark': raw.c_ref_dark,
                'c_sig_dark': raw.c_sig_dark,
                'a_ref': a_ref,
                'a_sig': a_sig,
                'c_ref': c_ref,
                'c_sig': c_sig}




        #
        # data = (dt,
        #         a,
        #         c,
        #         a_wvls,
        #         c_wvls,
        #         cal.internal_temperature,
        #         cal.external_temperature,
        #         cal.flag_outside_calibration_range,
        #         raw.output_wavelength,
        #         raw.time_stamp,
        #         raw.t_int,
        #         raw.t_ext,
        #         raw.p,
        #         raw.frame_len,
        #         raw.frame_type,
        #         raw.a_ref_dark,
        #         raw.a_sig_dark,
        #         raw.c_ref_dark,
        #         raw.c_sig_dark,
        #         a_ref,
        #         a_sig,
        #         c_ref,
        #         c_sig,
        #         self._cal_file,
        #         self._real_sn)

        return data

    def disconnect(self):
        self.rs232.disconnect()



