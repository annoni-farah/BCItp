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

from utils import *

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

    def run(self):

        self.HWStream()
        
    def StoreData(self, new_data):
         
        data = np.array(new_data) # transform list into numpy array
        self.all_data = np.vstack((self.all_data, data)) # append to data stack
    
    def PrintData(self, data):
        
        print data
        
        
    def SaveData(self, path):
        
        self.all_data = np.delete(self.all_data, (0), axis = 0)

        saveDataAsTxt(self.all_data, path)

        self.all_data = np.empty([self.n_channels]) # erase all_data content

    def HWStream(self):

        if self.acq_mode == 'openbci':

            import open_bci_v3 as bci

            self.board = bci.OpenBCIBoard(port=p, baud=b)
            self.board.start_streaming(self.GetData) # start getting data from amplifier

        elif self.acq_mode == 'simu':

            import open_bci_simu as bci

            self.board = bci.OpenBCIBoard(port=p, baud=b)
            self.board.start_streaming(self.GetData) # start getting data from amplifier

        elif self.acq_mode == 'playback':

            import open_bci_playback as bci

            self.LoadDataAsMatrix(self.playback_path)

            self.board = bci.OpenBCIBoard(port=p, baud=b, data=self.loadedData)
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

    def Stop(self):
        print 'Streaming stopped. Closing connection to hardware'
        self.board.stop()
        self.board.disconnect()
        self._stop.set()

    def Stopped(self):
        return self._stop.isSet()

    def updateCircBuf(self, data):

        self.circBuff.append(data)

    def MarkEvents(self, ev_type):

        new = np.array([self.sample_counter, ev_type])
        self.event_list = np.vstack((self.event_list, new))

    def SaveEvents(self, path):

        self.event_list = np.delete(self.event_list, (0), axis = 0)

        saveDataAsTxt(self.event_list, path)

        # erase all_data content
        self.all_data = np.empty([self.n_channels]) 
        self.event_list = np.array([0,0])

    def CreateDataProcessing(self, buf_len, f_low, f_high, f_order):

        self.all_data = np.empty([self.n_channels])

        self.energy_history = collections.deque(maxlen = 20)

        self.circBuff = collections.deque(maxlen = buf_len) # create a qeue 

        self.dp = DataProcessing(f_low, f_high, self.board.getSampleRate(), f_order)

        self.event_list = np.array([0,0])

    def CalcEnergyAverage(self, channel_list):
        
        eh = np.array(self.energy_history)

        energy_ch = eh[:,channel_list]

        avg_smp = sum(energy_ch) / energy_ch.shape[0]

        avg_ch = sum(avg_smp) / len(avg_smp)
        
        return avg_ch

    def ComputeEnergy(self, channel_list):
        raw_data = np.array(self.circBuff)

        if raw_data.shape[0] > 125:

            filt_data = self.dp.ApplyFilter(raw_data.T).T

            e = self.dp.ComputeEnergy(filt_data)

            energy = sum(e[channel_list]) / len(e[channel_list])

            self.energy_history.append(e)

            return energy
        else:
            return 0









