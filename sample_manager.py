#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from threading import Thread
import numpy as np
import os
from time import sleep

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'

#define a classe manager
class SampleManager:
    def __init__(self):            
        pass
        
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
        
       
      
if __name__ == '__main__': # this code is only executed if this module is not imported

    # Reset variables at every run
    
    sm = SampleManager()    
    
    pass
    def get_data(sample):
        '''Get the data from amplifier and push it into the circular buffer.
        Also implements a counter to plot against the read value
        ps: This function is called by the OpenBci start_streaming() function'''
        indata =  sample.channel_data
        sm.PrintData(indata)
        sm.StoreData(indata)
    
    

    # OpenBCI config
    port = '/dev/ttyUSB1'  # port which opnbci is connected (linux). windows = COM1
    baud = 115200
    board = bci.OpenBCIBoard(port=port, baud=baud)
    
    sleep(1) # need to include this to wait for test config setup
    
    try:
        board.start_streaming(get_data) # start getting data from amplifier
		
    except:
        board.stop()
        board.disconnect()
