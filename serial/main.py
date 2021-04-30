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
        self.pacStart = b'$'
        self.pacStop = b';'

    def readPackages(self):
        if self.port.inWaiting():
            c = self.port.read()
            # print(c)
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
                self.buffer.append(c.decode('ascii'))
                self.bufferCounter = self.bufferCounter+1
        return False

    def data(self):
        return self.buffer

    def sendPackages(self, data):
        pack = '$125;'
        print(pack)
        self.port.write(pack.encode('utf8'))

    def close(self):
        self.port.close()


uart = Uart(s_uart)


try:
    while 1:
        if uart.readPackages():
            print("read " + str(uart.bufferCounter) + " : " + str(uart.data()))
        time.sleep(0.8)
        uart.sendPackages('125')

finally:
    uart.close()
