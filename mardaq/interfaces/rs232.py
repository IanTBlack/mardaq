import serial
import time

from mardaq.core import console_logger


class RS232():
    def __init__(self):
        self.console_log = console_logger(2)
        self._serial = serial.Serial()


    def __enter__(self):
        return self


    def __exit__(self,et, ev, etb):
        self.disconnect()

    def connect(self, port, baudrate, bytesize = 8, parity = 'N', stopbits = 1, flowcontrol = 0, timeout = 1):
        self._serial.port = port
        self._serial.baudrate = int(baudrate)
        self._serial.bytesize = bytesize
        self._serial.parity = parity
        self._serial.stopbits = stopbits
        self._serial.xonxoff = flowcontrol
        self._serial.timeout = int(timeout)
        try:
            self._serial.open()
            self.console_log.debug(f"Connected to port {port} at {baudrate} bps.")
            return True
        except ConnectionError:
            self.console_log.error(f"Unable to connect to device on port {port}.")
            raise serial.PortNotOpenError()


    def clear_buffers(self):
        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()
        self.console_log.debug(f'Cleared serial buffers on port {self._serial.port}.')


    def read_buffer(self):
        buffer = self._serial.read(self._serial.in_waiting)
        return buffer

    def disconnect(self):
        self._serial.close()