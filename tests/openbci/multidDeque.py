#!/usr/bin/env python2.7.
# import sys; sys.path.append('..') # help python find open_bci_v3.py relative to scripts folder
import open_bci_simu as bci
import matplotlib.pyplot as plt # for plot
import collections # circular buffer
from time import sleep # sleep functions
from threading import Thread

import numpy as np
# Gets data from one channel of OpenBci and plots the data in real time.
# Author: Rafael Duarte

# Global variables
i = 0
bufflen = 1000 # Circular buffer setup
dataBuff = collections.deque(maxlen = bufflen) # create a qeue 
tempBuff = collections.deque(maxlen = bufflen) # create a qeue 
fa = 250 # sample frequency (approx)


class PlotData(Thread):
    '''Plot the data in a different thread to avoid sample discarding. If the plotting is done
    within the main loop, the amplifier will push samples through serial port and we will not 
    not have enough time to process it -> sample loss'''

    def __init__(self):  # executed on instantiation of the class PlotData
        Thread.__init__(self)

    def run(self):
        # Plot figure setup
        plt.ion()
        plt.show()
        plt.hold(False) # hold is off
        global tempBuff
        global dataBuff

        sleep(3)

        CHANNEL = 0
        while True:

            data = dataBuff
            npdata = np.array(data)[:,CHANNEL]

            ts = np.array(tempBuff)

            plt.plot(ts, npdata, linewidth=3)
            plt.axis([ts[0], ts[-1], -3000, 3000])
            plt.xlabel('Sample Count')
            plt.ylabel('Voltage on Channel')
            plt.grid(True)
            plt.draw()

def get_data(sample):
    '''Get the data from amplifier and push it into the circular buffer.
    Also implements a counter to plot against the read value
    ps: This function is called by the OpenBci start_streaming() function'''

    global i # the counter is global
    i += 1
    dataBuff.append(sample.channel_data)
    tempBuff.append(i)

# Main loop
if __name__ == '__main__': # this code is only executed if this module is not imported
    # Channel which will be plotted
    channel = 1; 
    pltdata = PlotData()
    pltdata.daemon = True # just to interrupt both threads at the end
    pltdata.start() # starts running the plot_data thread

    port = '/dev/ttyUSB0' # port which opnbci is connected (linux). windows = COM1
    baud = 115200
    board = bci.OpenBCIBoard(port=port, baud=baud)
    sleep(1) # need to include this to wait for test config setup
    board.start_streaming(get_data) # start getting data from amplifier

