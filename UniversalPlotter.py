import sys

import matplotlib.lines
import matplotlib.pyplot as plt
import matplotlib.animation as animate
import tkinter.filedialog as fdial
import math
import pandas as pd


class UniversalPlotter:
    figure = plt.figure()
    filename:str = ''
    plots_to_make:list = []
    axes:list = []
    lines:list = []

    def __init__(self,file,plots:list) -> None:
            self.filename = file
            self.plots_to_make = plots
            columns = 2
            rows = math.ceil(len(self.plots_to_make)/2)
            for i in range(len(self.plots_to_make)):
                subplot = self.figure.add_subplot(rows,columns,i+1)
                line, = subplot.plot([],[],marker = 'o')
                self.axes.append(subplot)
                self.lines.append(line)
    def startPlot(self):
        try:
            live_plot = animate.FuncAnimation(self.figure,self.HAndle_Plots,cache_frame_data=False,interval=1000)
            plt.show()
        except KeyboardInterrupt:
            print('Plotting stopped by user.')
    def HAndle_Plots(self,i)->None:
        data = pd.read_csv(self.filename)
        for i in range(len(self.plots_to_make)):
            plot_parameters = self.plots_to_make[i].split(',')
            self.lines[i].set_data(data.loc[:,plot_parameters[0]],data.loc[:,plot_parameters[1]])
            self.axes[i].relim()
            self.axes[i].autoscale_view()
            self.axes[i].set_xlabel(plot_parameters[0])
            self.axes[i].set_ylabel(plot_parameters[1])
        self.figure.tight_layout()
def main() -> None:
    plot = UniversalPlotter(sys.argv[1],sys.argv[2:])
    plot.startPlot()


if __name__ == "__main__":
    main()