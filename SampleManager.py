#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from threading import Thread
import numpy as np
import os
from time import sleep
import open_bci_simu as bci

from math import ceil

import threading

import collections # circular buffer

from DataProcessing import DataProcessing

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'

#define a classe manager
class SampleManager(threading.Thread):
    def __init__(self, p, b, rec = False ):
        super(SampleManager, self).__init__()
        self._stop = threading.Event()            
        
        self.sample_counter = 0

        self.stop_flag = False

        self.rec_flag = rec

        self.board = bci.OpenBCIBoard(port=p, baud=b)

    def run(self):

        self.HWStream()
        
    def StoreData(self, new_data):
         

        data = np.array(new_data)[:,0] # transform list into numpy array
        self.all_data = np.vstack((self.all_data, data)) # append to data stack
    
    def PrintData(self, data):
        
        print data
        
        
    def SaveData(self):
        
        # file = open('data/rafael" + "/precal_config.txt','a')
        
        # np.savetxt(file, self.all_data)       # Save data to txt file   
        
        # file.close()
        self.all_data = np.delete(self.all_data, (0), axis = 0)

        with open("data/rafael" + "/data_cal.txt", "a") as data_file:    
            np.savetxt(data_file, self.all_data)

        self.all_data = np.empty([8]) # erase all_data content
        
    def LoadDataAsMatrix(self, user, cols=[]):
        """Loads text file content as numpy matrix
        Parameters
        ----------
        path : path to text file
        
        cols : order of columns to be read
    
        Returns
        -------
        matrix : numpy matrix, shape as written in txt
    
        Examples
        --------
        >>> data_path = "/PATH/TO/FILE/somematrix.txt"
        >>> matrix_data = loadAsMatrix(data_path)
        """
        
        path = PATHTOUSERS + user + "DATA.TXT"     
        
        if cols == []:
            matrix = np.loadtxt(open(path,"rb"), skiprows=1)
            
        else:
            matrix = np.loadtxt(open(path,"rb"), skiprows=1, usecols=cols)
    
        return matrix

    def HWStream(self):
        # OpenBCI config

        self.board.start_streaming(self.GetData) # start getting data from amplifier
        

    def GetData(self, sample):
        '''Get the data from amplifier and push it into the circular buffer.
        Also implements a counter to plot against the read value
        ps: This function is called by the OpenBci start_streaming() function'''
        indata =  sample.channel_data
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

    def ComputeEnergy(self, channel_list):
        raw_data = np.array(self.circBuff)[:,channel_list]

        if raw_data.shape[0] > 125:

            filt_data = self.dp.ApplyFilter(raw_data.T).T

            e = self.dp.ComputeEnergy(raw_data)

            energy = sum(e)/len(e)

            self.energy_history.append(energy)

            return energy
        else:
            return 0

    def MarkEvents(self, ev_type):

        new = np.array([self.sample_counter, ev_type])
        self.event_list = np.vstack((self.event_list, new))

    def SaveEvents(self):

        self.event_list = np.delete(self.event_list, (0), axis = 0)

        with open("data/rafael" + "/events_cal.txt", "a") as data_file:    
            np.savetxt(data_file, self.event_list)

        self.all_data = np.empty([8]) # erase all_data content
        self.event_list = np.array([0,0])

    def CreateDataProcessing(self, ch, buf_len, f_low, f_high, f_order):

        self.channels = ch

        self.all_data = np.empty([8])

        self.energy_history = collections.deque(maxlen = 20)

        self.circBuff = collections.deque(maxlen = buf_len) # create a qeue 

        self.dp = DataProcessing(f_low, f_high, self.board.getSampleRate(), f_order)

        self.event_list = np.array([0,0])

    def CalcEnergyAverage(self):
        
        avg = ceil(100 * sum(self.energy_history) / len(self.energy_history))
        
        return avg









