# simple serial monitor
# include two regimes console and monitor
# vps.dmmi@gmail.com

from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import *
from random import *
import numpy
import math
import sys
import glob
import serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

WBC = 20
WBM = 30

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result



# start windows
root = Tk()

# create tabs
note = ttk.Notebook(root)
#note.pack(side=TOP, fill=X)
note.grid(column=0, row=0, columnspan=3)
tabConsole = Frame(note)
tabMonitor = Frame(note)
note.add(tabConsole, text="serial console")
note.add(tabMonitor, text="serial monitor")

# function of check current tab
def findTab(event):
    print(note.tabs().index(note.select()))

note.bind("<<NotebookTabChanged>>", findTab)


# status bar
comboSerials = ttk.Combobox(root, values=serial_ports())
comboSerials.grid(column=0, row=1)
comboSerials.current(0)
#print(comboSerials.current(), comboSerials.get())

serial_speeds = ['1843200', '921600', '460800', '230400', '115200', '57600', '38400', '19200', '9600', '4800', '2400', '1200', '600', '300', '150', '100', '75', '50'] #Скорость COM порта
comboSpeed = ttk.Combobox(root, values=serial_speeds)
comboSpeed.grid(column=1, row=1)
comboSpeed.current(8)

buttonConnect = Button(root, text="Connect", bg="light grey")
buttonConnect.grid(column=2, row=1)
fConnect = False

def connectUart():
    global ser
    global fConnect

    if not fConnect:
        ser = serial.Serial(
            port=comboSerials.get(),
            baudrate=int(comboSpeed.get()),
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            # timeout=0.5, # IMPORTANT, can be lower or higher
            # inter_byte_timeout=0.1 # Alternative
        )
        print(ser)
        buttonConnect['text'] = "Connected"
        fConnect = True

    else:
        print('disconnect')
        fConnect = False
        buttonConnect['text'] = "Connect"
        ser.close()

buttonConnect['command'] = connectUart


# organize tab 1
frameConsole = Frame(tabConsole, bd=5, width=WBM)
frameConsole.pack(side=TOP)




# organize tab monitor
frameMonitor = Frame(tabMonitor, bd=5)
frameMonitor.pack()
# add animation plt
fig = plt.Figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.25)
ti = 0
g1 = [0]
gt = [ti]
grf, = ax.plot(gt, g1, 'r')

canvas = FigureCanvasTkAgg(fig, master=frameMonitor)
canvas.get_tk_widget().pack()



def update():
    global ti
    _cur = random()
    g1.append(_cur)
    gt.append(ti)
    ti = ti + 1

    grf.set_data(gt, g1)
    # Update axis
    ax = canvas.figure.axes[0]
    ax.set_xlim(min(gt), ti)
    ax.set_ylim(min(g1) - 1, max(g1) + 1)
    canvas.draw()

    root.after(300, update)


root.after(300, update())


root.mainloop()
