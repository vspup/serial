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

print(serial_ports())

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
comboExample = ttk.Combobox(root, values=serial_ports())

print(dict(comboExample))
comboExample.grid(column=0, row=1)
comboExample.current(0)

bar=Button(root, text="off", bg="light grey")
bar.grid(column=2, row=1)



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
