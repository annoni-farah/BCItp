#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from threading import Thread
import numpy as np
import os
from time import sleep
import open_bci_simu as bci

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'

#define a classe manager
class SampleManager:
    def __init__(self):            
        
        NCHANNELS = 8
        self.all_data = np.empty([NCHANNELS])     
        
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

    def hw_stream(self):
        # OpenBCI config
        port = '/dev/ttyUSB0'  # port which opnbci is connected (linux). windows = COM1
        baud = 115200
        board = bci.OpenBCIBoard(port=port, baud=baud)

        board.start_streaming(self.get_data) # start getting data from amplifier
        

    def get_data(self, sample):
        '''Get the data from amplifier and push it into the circular buffer.
        Also implements a counter to plot against the read value
        ps: This function is called by the OpenBci start_streaming() function'''
        indata =  sample.channel_data
        self.PrintData(indata)
        # self.StoreData(indata)
