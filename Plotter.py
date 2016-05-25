
import threading
import matplotlib.pyplot as plt # for plot

from time import sleep

class Figure(threading.Thread):
    '''Plot the data in a different thread to avoid sample discarding. If the plotting is done
    within the main loop, the amplifier will push samples through serial port and we will not 
    not have enough time to process it -> sample loss'''

    def __init__(self):  # executed on instantiation of the class PlotData

        super(Figure, self).__init__()

        self._stop = threading.Event()            

        self.x_data = []
        self.y_data = []

    def run(self):

        # Plot figure setup
        # if ~self.stop_flag:
        plt.ion()
        plt.show()
        plt.hold(False) # hold is off
            
        while True:
            if len(self.y_data) > 125:

                if self.stop_flag:
                    self.Stop()

                # else:
                plt.plot(self.x_data, self.y_data, linewidth=3)
                plt.axis([self.x_data[0], self.x_data[-1], -300, 300])
                plt.xlabel('Sample Count')
                plt.ylabel('Voltage on Channel')
                plt.grid(True)
                plt.draw()
                    


    def fillBuffer(self, x, y):

        self.x_data = x
        self.y_data = y

    def Stop(self):
        self._stop.set()

    def Stopped(self):
        return self._stop.isSet()

    def join(self, timeout=None):
        """ Stop the thread and wait for it to end. """
        plt.close()
        self._stop.set( )
        threading.Thread.join(self, timeout)


        

    


