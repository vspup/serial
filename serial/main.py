# simple serial monitor
# vps.dmmi@gmail.com

import serial
import time

# name of serial port
uart = 'COM16'

def read(port):
    t = time.time()
    read_buffer = b''
    t_wait = 0.8

    job = True
    while job:
        if time.time() < t + t_wait:
            if port.inWaiting():
                c = port.read()  # attempt to read a character from Serial
                if c == b'\r':
                    read_buffer += c
                    pass

                elif c == b'\n':
                    read_buffer += c  # add the newline to the buffer
                    job = False

                else:
                    read_buffer += c  # add to the buffer

        else:
            read_buffer = ""
            job = False

    return read_buffer