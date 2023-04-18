from mardaq.core import *

class EZO():
    """
    A simple class for reading and writing data to any Atlas Scientific EZO.
    """
    def __init__(self, address, bus=1):
        self.addr = address
        self.i2c_read = io.open(file="/dev/i2c-{}".format(bus),mode="rb",buffering=0)
        self.i2c_write = io.open(file="/dev/i2c-{}".format(bus),mode="wb",buffering=0)
        time.sleep(0.5)
        fcntl.ioctl(self.i2c_read, 0x703, self.addr)
        fcntl.ioctl(self.i2c_write, 0x703, self.addr)
        time.sleep(0.5)


    def send_cmd(self,cmd):
        cmd += "\00"
        self.i2c_write.write(cmd.encode())

    def read_response(self,num_bytes = 32):
        raw = self.i2c_read.read(num_bytes)
        return raw

