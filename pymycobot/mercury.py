# coding=utf-8

import time
import threading
import serial
import serial.serialutil


from pymycobot.mercury_api import MercuryCommandGenerator
from pymycobot.error import calibration_parameters


class Mercury(MercuryCommandGenerator):
    def __init__(self, port, baudrate="115200", timeout=0.1, debug=False):
        """
        Args:
            port     : port string
            baudrate : baud rate string, default '115200'
            timeout  : default 0.1
            debug    : whether show debug info
        """
        super(Mercury, self).__init__(debug)
        self.calibration_parameters = calibration_parameters

        self._serial_port = serial.Serial()
        self._serial_port.port = port
        self._serial_port.baudrate = baudrate
        self._serial_port.timeout = timeout
        self._serial_port.rts = False
        self._serial_port.open()
        self.lock = threading.Lock()
        self.lock_out = threading.Lock()
        self.has_reply_command = []
        self.is_stop = False
        self.read_threading = threading.Thread(target=self.read_thread)
        self.read_threading.daemon = True
        self.read_threading.start()
        try:
            self._serial_port.write(b"\xfa")
        except serial.serialutil.SerialException as e:
            self._serial_port.close()
            time.sleep(0.5)
            self._serial_port = serial.Serial()
            self._serial_port.port = port
            self._serial_port.baudrate = baudrate
            self._serial_port.timeout = timeout
            self._serial_port.rts = False
            self._serial_port.open()
        self.get_limit_switch()

    def open(self):
        self._serial_port.open()
        
    def close(self):
        self._serial_port.close()
