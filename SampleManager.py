#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from threading import Thread
import numpy as np
import os
from time import sleep

from math import ceil

import threading

import collections # circular buffer

from DataProcessing import DataProcessing

from utils import saveMatrixAsTxt
from utils import LoadDataAsMatrix

import open_bci_v3 as bci
import open_bci_simu as simulator
import open_bci_playback as playback

from Plotter import Figure

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'

#define a classe manager
class SampleManager(threading.Thread):
    def __init__(self, p, b, ch, mode = 'openbci' , path = None, rec = False):
        super(SampleManager, self).__init__()

        self.channels = ch

        self.n_channels = len(self.channels)

        self._stop = threading.Event()            
        
        self.sample_counter = 0

        self.stop_flag = False

        self.acq_mode = mode

        self.rec_flag = rec

        self.playback_path = path

        if self.acq_mode == 'openbci':

            self.board = bci.OpenBCIBoard(port=p, baud=b)

        elif self.acq_mode == 'simu':

            self.board = simulator.OpenBCIBoard(port=p, baud=b)

        elif self.acq_mode == 'playback':

            loadedData = LoadDataAsMatrix(self.playback_path)

            self.board = playback.OpenBCIBoard(port=p, baud=b, data=loadedData)

    def run(self):

        self.HWStream()
        
    def StoreData(self, new_data):
         
        data = np.array(new_data) # transform list into numpy array
        self.all_data = np.vstack((self.all_data, data)) # append to data stack
    
    def PrintData(self, data):
        
        print data
        
    def SaveData(self, path):
        
        self.all_data = np.delete(self.all_data, (0), axis = 0)

        saveMatrixAsTxt(self.all_data, path)

        self.all_data = np.empty([self.n_channels]) # erase all_data content

    def HWStream(self):

        self.board.start_streaming(self.GetData) # start getting data from amplifier


    def GetData(self, sample):
        '''Get the data from amplifier and push it into the circular buffer.
        Also implements a counter to plot against the read value
        ps: This function is called by the OpenBci start_streaming() function'''
        indata =  [sample.channel_data[x] for x in self.channels]
        self.updateCircBuf(indata);
        
        if self.rec_flag:
            self.StoreData(indata)

        self.sample_counter += 1

        if(self.stop_flag):
            self.Stop()

    def GetBuffData(self, filt = False):
        t = np.array(self.tBuff)
        d = np.array(self.circBuff)

        if d.shape[0] > 125:
            filt_d = self.dp.ApplyFilter(d.T).T
            return t, filt_d
        else:
            return t, float('NaN')


    def Stop(self):
        print 'Streaming stopped. Closing connection to hardware'
        self.board.stop()
        self.board.disconnect()
        self._stop.set()

    def Stopped(self):
        return self._stop.isSet()

    def updateCircBuf(self, data):

        self.circBuff.append(data)
        self.tBuff.append(self.sample_counter)

    def MarkEvents(self, ev_type):

        new = np.array([self.sample_counter, ev_type])
        self.event_list = np.vstack((self.event_list, new))

    def SaveEvents(self, path):

        self.event_list = np.delete(self.event_list, (0), axis = 0)

        saveMatrixAsTxt(self.event_list, path)

        # erase all_data content
        self.all_data = np.empty([self.n_channels]) 
        self.event_list = np.array([0,0])

    def CreateDataProcessing(self, buf_len, f_low, f_high, f_order):

        self.all_data = np.empty([self.n_channels])

        self.energy_history = collections.deque(maxlen = 20)

        self.circBuff = collections.deque(maxlen = buf_len) # create a qeue for input data
        self.tBuff = collections.deque(maxlen = buf_len) # create a qeue for time series

        self.dp = DataProcessing(f_low, f_high, self.board.getSampleRate(), f_order)

        self.event_list = np.array([0,0])

    def CalcEnergyAverage(self, channel_list):
        
        eh = np.array(self.energy_history)

        energy_ch = eh[:,channel_list]

        avg_smp = np.mean(energy_ch)

        avg_ch = np.mean(avg_smp)
        
        return avg_ch

    def ComputeEnergy(self, channel_list):
        raw_data = np.array(self.circBuff)

        if raw_data.shape[0] > 125:

            filt_data = self.dp.ApplyFilter(raw_data.T).T

            e = self.dp.ComputeEnergy(filt_data)

            energy = np.mean(e[channel_list])

            self.energy_history.append(e)

            return energy
        else:
            return 0

    def SetupFig(self):

        self.fig = Figure()
        self.fig.daemon = True # just to interrupt both threads at the end
        self.fig.stop_flag = False
        self.fig.start() # starts running the plot_data thread

    def UpdateFigBuffer(self):

        t = np.array(self.tBuff)
        d = np.array(self.circBuff)

        if d.shape[0] > 125:
            filt_d = self.dp.ApplyFilter(d.T).T

            self.fig.fillBuffer(t, filt_d)

    def CloseFig(self):
        # self.fig.Stop()
        # self.fig.join()
        self.fig.stop_flag = True
        self.fig.join()
        












