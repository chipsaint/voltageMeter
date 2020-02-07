#import glob as glob
#print(glob.glob("*.csv"))
import tkinter as tk
import csv
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import glob as glob

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


root = tk.Tk()
root.wm_title("Voltage Sensor Data Viewer")
filesList = glob.glob("*.csv")
tkvar = tk.StringVar(root)
status = tk.StringVar(root)

EM3Value = []
EM3Time = []
EM2Value = []
EM2Time = []
EM1Value = []
EM1Time = []
data = []

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def clearData():
    EM3Value.clear()
    EM3Time.clear()
    EM2Value.clear()
    EM2Time.clear()
    EM1Value.clear()
    EM1Time.clear()
    data.clear()

def getAllData():
    for i in range(0,len(filesList)):
        tkvar.set(filesList[i])
        getData()
        clearData()
    status.set('All plots saved.')

def getData():
    lwidth = 0.75
    filename = str(tkvar.get())
    filedate = filename[0:8]
    #filedate = input("Enter date file (YYYYMMDD): ")

    with open(filename,'r') as file:
        data = list(csv.reader(file,delimiter=","))
    print("Opened", filename)
    print("Successfully read", len(data),"data points")

    dataDate = data[0][0]
    dataDate = dataDate[:10]
    dataDay = data[0][1]
    title = dataDate +" "+ dataDay
    print('Preparing data for: '+title)

    print('Sorting Data')
    for x in range(0,len(data)):
        dataTime = data[x][0]
        #print(dataTime)
        dataTime = datetime.strptime(dataTime, '%Y-%m-%d %H:%M:%S')
        timestamp = matplotlib.dates.date2num(dataTime)
        try:
            valueNow = float(data[x][3])
            if data[x][2] == 'EM1-V':
                EM1Value.append(valueNow)
                EM1Time.append(timestamp)
            if data[x][2] == 'EM2-V':
                EM2Value.append(valueNow)
                EM2Time.append(timestamp)
            if data[x][2] == 'EM3-V':
                EM3Value.append(valueNow)
                EM3Time.append(timestamp)
        except:
            pass
    EM3ValueA = np.array(EM3Value)
    EM2ValueA = np.array(EM2Value)
    EM1ValueA = np.array(EM1Value)


    #PLOT THE GRAPH
    print('Plotting Data')

    """
    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
    """
    plt.clf()
    plt.ylim(200,260)
    plt.title(title)
    plt.xlabel('Time (HH:MM:SS)')
    plt.ylabel('Voltage (V)')
    plt.plot_date(EM1Time,EM1ValueA,linestyle='-',label='EM1-V',ms=0,linewidth=lwidth,color='green')
    plt.plot_date(EM2Time,EM2ValueA,linestyle='-',label='EM2-V',ms=0,linewidth=lwidth,color='red')
    plt.plot_date(EM3Time,EM3ValueA,linestyle='-',label='EM3-V',ms=0,linewidth=lwidth,color='blue')
    plt.gcf().autofmt_xdate(rotation=90)
    dateFMT = mdates.DateFormatter('%H:%M:%S')
    plt.gca().xaxis.set_major_formatter(dateFMT)
    plt.subplots_adjust(left=0.05,right=0.98,top=0.9,bottom=0.2)
    plt.axhline(220,linestyle='--',color='gray',linewidth=lwidth)
    plt.axhline(240,linestyle='--',color='gray',linewidth=lwidth)
    plt.grid(which='major',axis='x',linestyle='--',color='gray',linewidth=lwidth)
    plt.legend(fontsize='small',loc='upper right')

    status.set('Figure saved as '+filedate+'.png')
    print('Figure saved as '+filedate+'.png')
    plt.savefig(filedate+'.png')
    np.delete(EM1ValueA,[0])
    np.delete(EM2ValueA,[0])
    np.delete(EM3ValueA,[0])
    print('Cleared ARRAY')


tkvar.set('Select File')
status.set('Ready')
f = tk.Frame(root)
popupMenu = tk.OptionMenu(f, tkvar, *filesList)
popupMenu.pack(padx=5, pady=10,side=tk.LEFT)
button = tk.Button(master=f, text="View Data", command=getData)
button.pack(padx=5, pady=10,side=tk.LEFT)
statusBar = tk.Label(master=f,textvariable=status,width=50, anchor='w')
statusBar.pack(side=tk.LEFT,pady=10,padx=5)
exitbutton = tk.Button(master=f, text="Exit Program", command=_quit)
exitbutton.pack(padx=5, pady=10,side=tk.RIGHT)
getAllButton = tk.Button(master=f, text = "Plot All Data",command=getAllData)
getAllButton.pack(padx=5,side=tk.RIGHT)

f.pack(side = tk.TOP)


fig = plt.figure(figsize=(15,5))
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect("key_press_event", on_key_press)

def change_dropdown(*args):
    filename = str(tkvar.get())
    return filename

def update():
    statusBar = tk.Label(master=root,textvariable=status)

tk.mainloop()
