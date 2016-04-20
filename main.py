# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:58:38 2016

@author: rafael
"""

#from sample_manager import * 
import sample_manager
import open_bci_simu as bci
from imp import reload

import GUI

# Force modules to be reloaded every time the code is run
sample_manager = reload(sample_manager)
bci = reload(bci)

def get_data(sample):
    '''Get the data from amplifier and push it into the circular buffer.
    Also implements a counter to plot against the read value
    ps: This function is called by the OpenBci start_streaming() function'''
    data = sample.channel_data
    sm.PrintData(data)
    sm.StoreData(data)
    


sm = sample_manager.SampleManager()
# OpenBCI config
port = '/dev/ttyUSB0'  # port which opnbci is connected (linux). windows = COM1
baud = 115200
board = bci.OpenBCIBoard(port=port, baud=baud)

gui = GUI.user_interface()

try:
#        board.start_streaming(get_data) # start getting data from amplifier
    board.start_streaming(get_data) # start getting data from amplifier

except:
    print "Interrupted by user..."    
    board.stop()
    board.disconnect()
    
    print "Saving recorded data"
    sm.SaveData("rafael")