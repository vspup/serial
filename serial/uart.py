# function uart
# vps.dmmi@gmail.com

import serial
import serial.tools.list_ports
import time

class Uart:
    def __init__(self):
        # get list of uart available
        self.ports = serial.tools.list_ports.comports()
        self.listUart = []
        for port, desc, hwid in sorted(self.ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            self.listUart.append(port)
        print(self.listUart)
        self.currentPort = 0
        self.buffer = b''


    def getListPort(self):
        return self.listUart


    def connectPort(self, name, baudrate):
        self.currentPort = serial.Serial(
            port=name,
            baudrate=int(baudrate),
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            # timeout=0.5, # IMPORTANT, can be lower or higher
            # inter_byte_timeout=0.1 # Alternative
        )


    def getCurrentPort(self):
        return self.currentPort


    def disconnectPort(self):
        self.currentPort.close()
        self.currentPort = 0


    def readlnPort(self):
        t = time.time()
        self.buffer = b''
        t_wait = 0.8
        count = 0
        if self.currentPort == 0:
            job = False
        else:
            job = True
        while job:
            if time.time() < t + t_wait:
                if self.currentPort.inWaiting():
                    c = self.currentPort.read()  # attempt to read a character from Serial
                    if c == b'\r':
                        pass
                    elif c == b'\n':
                        pass  # add the newline to the buffer
                        job = False
                    else:
                        self.buffer += c  # add to the buffer
                        count += 1
            else:
                self.buffer = b''
                job = False
        return count

    def getBuffer(self):
        return self.buffer

    #def parse(self):

