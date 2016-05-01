#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from threading import Thread
import numpy as np
import os
from time import sleep
import open_bci_simu as bci

import threading

import collections # circular buffer

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'

#define a classe manager
class SampleManager(threading.Thread):
    def __init__(self):
        super(SampleManager, self).__init__()
        self._stop = threading.Event()            
        
        NCHANNELS = 8
        self.all_data = np.empty([NCHANNELS])

        BUFFLEN = 1000 # Circular buffer setup
        self.circBuff = collections.deque(maxlen = BUFFLEN) # create a qeue 

        self.stop_flag = False

        port = '/dev/ttyUSB0'  # port which opnbci is connected (linux). windows = COM1
        baud = 115200
        self.board = bci.OpenBCIBoard(port=port, baud=baud)

        self.counter = 0

    def run(self):
        self.HWStream()
        
    def StoreData(self, new_data):
        
        data = np.array(new_data) # transform list into numpy array
        
        self.all_data = np.vstack((self.all_data, data)) # append to data stack
    
    def PrintData(self, data):
        
        print data
        
        
    def SaveData(self, user):
        
        file = open(PATHTOUSERS + user + '/' + 'DATA.txt','w')
        
        np.savetxt(file, self.all_data)       # Save data to txt file   
        
        file.close()
        
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
        # self.StoreData(indata)
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

    def ComputeEnergy(self):
        self.counter += 1
        return 1



