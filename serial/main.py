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

WBC = 20
WBM = 30

# start windows
root = Tk()

# create tabs
note = ttk.Notebook(root)
note.pack(side=TOP, fill=X)
tabConsole = Frame(note)
tabMonitor = Frame(note)
note.add(tabConsole, text="serial console")
note.add(tabMonitor, text="serial monitor")

# function of check current tab
def findTab(event):
    print(note.tabs().index(note.select()))

note.bind("<<NotebookTabChanged>>", findTab)


# status bar
bar=Button(root, text="off", bg="light grey")
bar.pack(side=BOTTOM, fill=X)

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
