import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animate
import tkinter.filedialog as fdial

import pandas as pd

filename = ""
def animation(i):
    data = pd.read_csv(filename,sep='\t')
    line1.set_data(data.loc[:,'Temperature'],data.loc[:,'Resistance'])
    line2.set_data(data.loc[:,'Mnum'],data.loc[:,'Resistance'])
    line3.set_data(data.loc[:,'Mnum'],data.loc[:,'Temperature'])
    ax1.set_xlabel('Temperature (°C)')
    ax1.set_ylabel('Resistance (Ohms)')
    ax1.set_title('Resistance vs. Temperature')
    ax2.set_xlabel('Measurement Number')
    ax2.set_ylabel('Resistance (Ohms)')
    ax2.set_title('Resistance vs. Measurement Number')
    ax3.set_xlabel('Measurement Number')
    ax3.set_ylabel('Temperature (°C)')
    ax3.set_title('Temperature vs. Measurement Number')
    ax3.grid(True)
    ax2.grid(True)
    ax1.grid(True)
    ax1.relim()
    ax2.relim()
    ax3.relim()
    ax1.autoscale_view(True, True, True)
    ax2.autoscale_view(True, True, True)
    ax3.autoscale_view(True, True, True)

if __name__ == "__main__":
    if len(sys.argv) != 1:
        filename = sys.argv[1]
    else:
        filename = fdial.askopenfilename()
    fig = plt.figure(figsize=(10, 6))
    # Top subplot: Resistance vs. Temperature
    ax1 = fig.add_subplot(2,1,1)
    line1, = ax1.plot([], [], marker='o', linestyle='-', color='b')
    ax1.set_xlabel('Temperature (°C)')
    ax1.set_ylabel('Resistance (Ohms)')
    ax1.set_title('Resistance vs. Temperature')
    ax1.grid(True)

    # Bottom-left subplot: Resistance vs. Measurement Number
    ax2 = fig.add_subplot(2,2,3)
    line2, = ax2.plot([], [], marker='o', linestyle='-', color='r')
    ax2.set_xlabel('Measurement Number')
    ax2.set_ylabel('Resistance (Ohms)')
    ax2.set_title('Resistance vs. Measurement Number')
    ax2.grid(True)

    # Bottom-right subplot: Temperature vs. Measurement Number
    ax3 = fig.add_subplot(2,2,4)
    line3, = ax3.plot([], [], marker='o', linestyle='-', color='g')
    ax3.set_xlabel('Measurement Number')
    ax3.set_ylabel('Temperature (°C)')
    ax3.set_title('Temperature vs. Measurement Number')
    ax3.grid(True)
    ani = animate.FuncAnimation(fig,animation,cache_frame_data=False,interval=1000,blit= False)
    plt.show()
