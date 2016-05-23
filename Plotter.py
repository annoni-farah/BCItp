
import threading
import matplotlib.pyplot as plt # for plot

from time import sleep

class Figure(threading.Thread):
    '''Plot the data in a different thread to avoid sample discarding. If the plotting is done
    within the main loop, the amplifier will push samples through serial port and we will not 
    not have enough time to process it -> sample loss'''

    def __init__(self):  # executed on instantiation of the class PlotData

        threading.Thread.__init__(self)

        self._stop = threading.Event()            

        self.x_data = []
        self.y_data = []

        self.stop_flag = False


    def run(self):

        # Plot figure setup
        plt.ion()
        plt.show()
        plt.hold(False) # hold is off
            
        while True:
            if len(self.y_data) > 125:

                plt.plot(self.x_data, self.y_data, linewidth=3)
                plt.axis([self.x_data[0], self.x_data[-1], -300, 300])
                plt.xlabel('Sample Count')
                plt.ylabel('Voltage on Channel')
                plt.grid(True)
                plt.draw()

                if self.stop_flag:
                    plt.close()
                    self._stop.set()
                    


    def fillBuffer(self, x, y):

        self.x_data = x
        self.y_data = y

    def Stop(self):
        self.stop_flag = True

    def Stopped(self):
        return self._stop.isSet()

    


