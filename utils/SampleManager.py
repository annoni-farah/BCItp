#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from threading import Thread
import numpy as np
import os
from time import sleep

from math import ceil, isnan

import threading

import collections # circular buffer

from DataProcessing import Filter

from utils import saveMatrixAsTxt
from utils import LoadDataAsMatrix

import open_bci_v3 as bci
import open_bci_simu as simulator
import open_bci_playback as playback

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'

#define a classe manager
class SampleManager(threading.Thread):
    def __init__(self, p, b, ch, buf_len, daisy = False, mode = 'openbci' , path = None):
        super(SampleManager, self).__init__()

        self.channels = ch

        self.n_channels = len(self.channels)

        self._stop = threading.Event()
        
        self.sample_counter = 0

        self.stop_flag = False

        self.acq_mode = mode

        self.playback_path = path

        self.buffer_length = buf_len

        self.energy_history = collections.deque(maxlen = 500)

        self.circBuff = collections.deque(maxlen = self.buffer_length) # create a qeue for input data
        self.tBuff = collections.deque(maxlen = self.buffer_length) # create a qeue for time series
        
        self.event_list = np.array([]).reshape(0,2)
        self.all_data = np.array([]).reshape(0,self.n_channels)

        if self.acq_mode == 'openbci':

            self.board = bci.OpenBCIBoard(port=p, baud=b, daisy=daisy)
            self.rec_flag = True

        elif self.acq_mode == 'simu':

            self.board = simulator.OpenBCIBoard(port=p, baud=b, daisy=daisy)
            self.rec_flag = True

        elif self.acq_mode == 'playback':
            
            self.rec_flag = False
            loadedData = LoadDataAsMatrix(self.playback_path)
            self.board = playback.OpenBCIBoard(port=p, baud=b, data=loadedData)

        self.sample_rate = self.board.getSampleRate()


    def run(self):

        self.HWStream()
        
    def StoreData(self, new_data):
         
        data = np.array(new_data) # transform list into numpy array
        self.all_data = np.vstack((self.all_data, data)) # append to data stack
    
    def PrintData(self, data):
        
        print data
        
    def SaveData(self, path):

        saveMatrixAsTxt(self.all_data, path, mode = 'w')

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

    def GetBuffData(self, mode = None):
        t = np.array(self.tBuff)
        d = np.array(self.circBuff)

        return t, d

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

        saveMatrixAsTxt(self.event_list, path, mode = 'w')
        











