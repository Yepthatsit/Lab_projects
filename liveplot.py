import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animate
import tkinter.filedialog as fdial

import pandas as pd

filename = ""
def animation(i):
    data = pd.read_csv(filename)
    line1.set_data(data.loc[:,'Time'],data.loc[:,'Pressure'])
    line2.set_data(data.loc[:,'Time'],data.loc[:,'Voltage'])
    line3.set_data(data.loc[:,'Pressure'],data.loc[:,'Voltage'])
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Pressure [bar]')
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Voltage [V]')
    ax3.set_xlabel('Pressure [bar]')
    ax3.set_ylabel('Voltage [V]')
    ax1.relim()
    ax2.relim()
    ax3.relim()
    ax1.autoscale_view(True, True, True)
    ax2.autoscale_view(True, True, True)
    ax3.autoscale_view(True, True, True)
    fig.tight_layout()
if __name__ == "__main__":
    if len(sys.argv) != 1:
        filename = sys.argv[1]
    else:
        filename = fdial.askopenfilename()
    fig = plt.figure(figsize=(10, 6))
    
    ax1 = fig.add_subplot(2,1,1)
    line1, = ax1.plot([], [], marker='o', linestyle='-', color='b')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Pressure [bar]')

    ax2 = fig.add_subplot(2,2,3)
    line2, = ax2.plot([], [], marker='o', linestyle='-', color='r')
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Voltage [V]')

    ax3 = fig.add_subplot(2,2,4)
    line3, = ax3.plot([], [], marker='o', linestyle='-', color='g')
    ax3.set_xlabel('Pressure [bar]')
    ax3.set_ylabel('Voltage [V]')
    fig.tight_layout()
    ani = animate.FuncAnimation(fig,animation,cache_frame_data=False,interval=1000,blit= False)
    plt.show()
