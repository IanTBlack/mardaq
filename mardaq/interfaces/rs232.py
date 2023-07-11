"""This is a higher level wrapper for the pyserial library that is optimized
for use with oceanographic sensors."""

import serial
import time


class RS232():
    def __init__(self):
        """Setup a blank serial object."""
        self.rs232 = serial.Serial()

    def connect(self, port, baudrate,
                bytesize=8, parity='N', stopbits=1, flowcontrol=0, timeout=1,
                verbose=False):
        """
        Connect to a port at the defined settings. Follows along with pyserial
        settings.
        Parameters
        ----------
        port : string
            An OS specific port identifier.
            Windows Example: 'COM11'
            Linux Example: '/dev/ttyUSB0'
        baudrate : int
            The baud rate of the sensor.
        bytesize : int, optional
            The number of data bits. The default is 8.
        parity : string, optional
            Identify the presence of a parity bit. The default is 'N'.
        stopbits : int, optional
            The number of bits to indicate a stop. The default is 1.
        flowcontrol : int, optional
            Consider port flow control. The default is 0.
        timeout : int, optional
            A pyserial specific parameter. The number of seconds to wait for
            a port to connect. The default is 1.
        verbose : bool, optional
            Used if you want messages printed to the console.
            The default is False.
        Returns
        -------
        bool
            True if the connection is successful. False if not.
        """
        self.rs232.port = port
        self.rs232.baudrate = int(baudrate)
        self.rs232.bytesize = bytesize
        self.rs232.parity = parity
        self.rs232.stopbits = stopbits
        self.rs232.xonxoff = flowcontrol
        self.rs232.timeout = int(timeout)
        try:
            self.rs232.open()
            if verbose is True:
                print('Connected on port {}.'.format(self.rs232.port))
            return True
        except ConnectionError:
            if verbose is True:
                print('Unable to connect on port {}.'.format(self.rs232.port))
            raise serial.PortNotOpenError()

    def disconnect(self, verbose=False):
        """
        Disconnect from the port.
        Parameters
        ----------
        verbose : bool, optional
            Used if you want messages printed to the console.
            The default is False.
        Returns
        -------
        bool
            True if the disconnect was successful. False if not.
        """
        try:
            self.rs232.close()
            if verbose is True:
                print('Disconnected from port {}.'.format(self.rs232.port))
            return True
        except ConnectionError:
            return False

    def status(self):
        """
        Check the status of the port.
        Returns
        -------
        bool
            True if open. False if not.
        """
        if self.rs232.is_open:
            return True
        elif self.rs232.is_open is False:
            return False

    def clear_buffers(self):
        """
        Clear the input and output buffers.
        From the perspective of the driving device, input is data being
        received from a sensor. Output is data being sent to a sensor.
        Returns
        -------
        None.
        """
        self.rs232.reset_input_buffer()
        self.rs232.reset_output_buffer()

    def write_command(self, command, EOL='\r\n', verbose=False):
        """
        Write an encoded command to the sensor.
        Parameters
        ----------
        command : string
            A sensor specific command.
            Example for SBE49. "DS"
        EOL : string, optional
            Append a set of end-of-line characters. May differ
            between sensors.
            The default is carriage return and line feed ('\r\n').
        verbose : bool, optional
            Used if you want messages printed to the console.
            The default is False.
        Returns
        -------
        None.
        """
        cmd = str.encode(command + EOL)
        self.rs232.write(cmd)
        time.sleep(0.010)
        if verbose is True:
            print('Command \"{}\" sent!'.format(command))

    def read_until(self, expected=None, size=None, timeout=None):
        """
        Parameters
        ----------
        expected : string, optional
            Can be specific string or a carriage return/linefeed.
            The default is '\r\n'.
        size : int, optional
            The number of bytes to read before stopping. The default is None.
        timeout : int, optional
            The number of seconds to allow the read to run until stopping.
            The default is None.
        Returns
        -------
        data : string
            An ASCII response from the sensor.
        """

        self.rs232._timeout = timeout
        if expected is None or expected == "":
            incoming = self.rs232.read_until("", size)
        else:
            incoming = self.rs232.read_until(bytes(expected.encode()), size)
        data = incoming.decode()
        return data

    def read(self, number_of_bytes):
        return self.rs232.read(number_of_bytes)

    def read_buffer(self):
        return self.rs232.read(self.rs232.in_waiting)

    def read_bytes(self, check_interval=0.1, read_timeout=60):
        self.check_interval = check_interval
        self.read_timeout = read_timeout
        self._input_buffer_check()
        data = self.read(self._buffer_length)
        return data

    def _input_buffer_check(self):
        """
        Continuously check the buffer X amount of seconds until the buffer
        value stays constant or a timeout occurs.
        Raises
        ------
        StopIteration
            Break the never ending loop if the time value exceeds 30 seconds.
        Returns
        -------
        None.
        """
        self._buffer_length = 0
        buffer = self.rs232.in_waiting
        start = time.monotonic()
        time.sleep(self.check_interval)
        while True:
            if (time.monotonic() - start) > self.read_timeout:
                raise StopIteration("Forced serial read timeout.")
            incoming = self.rs232.in_waiting
            if buffer == incoming:
                self._buffer_length = buffer
                break
            else:
                buffer = incoming
                time.sleep(self.check_interval)

    # ----------------------------------------------------------------------------#

    def read_until_stop(self, check_interval_ms=100, read_timeout=30):
        """
        Read until the buffer value stops changing. Typically used for situations where the response from the
        sensor is expected to be a single data point. Should not be implemented for sensors that continually send data.

        Parameters
        ----------
        check_interval_ms : int, optional
            The number of milliseconds to wait until a buffer check is
            performed again.The default is 100.
        Returns
        -------
        data : string
            An ASCII response from the sensor.
        """
        self.check_interval = check_interval_ms / 1000
        self.read_timeout = read_timeout
        self._input_buffer_check()  # Check the buffer until it stops.
        incoming = self.rs232.read(self._buffer_length)
        data = incoming.decode()
        return data