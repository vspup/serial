# simple serial monitor
# vps.dmmi@gmail.com

import serial
import time

# name of serial port
s_uart = 'COM11'



# class create gui to coil
class Uart:

    def __init__(self, s_serial):

        self.port = serial.Serial(
            port=s_serial,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            # timeout=0.5, # IMPORTANT, can be lower or higher
            # inter_byte_timeout=0.1 # Alternative
        )

        # variable for parsing
        self.buffer = []
        self.bufferCounter = 0
        self.fParsing = False
        self.pacStart = '$'
        self.pacStop = ';'

    def parsing(self):
        if self.port.inWaiting():
            c = self.port.read()
            # ignory return and new line
            if (c == b'\r') or (c == b'\n'):
                return False
            # packages end
            if c == self.pacStop:
                self.fParsing = False
                return True
            # start packages
            if c == self.pacStart:
                self.fParsing = True
                self.bufferCounter = 0
                self.buffer = []
                return False
            if self.fParsing:
                self.append(c)
                self.bufferCounter = self.bufferCounter+1
        return False

    def data(self):
        return self.buffer

    def close(self):
        self.port.close()


uart = Uart(s_uart)


try:
    while 1:
        if uart.parsing():
            print(uart.data())

finally:
    uart.close()
