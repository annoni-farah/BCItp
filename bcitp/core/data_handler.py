#!/usr/bin/env python
# -*- coding: utf-8 -*-

# KIVY PACKAGES
from kivy.logger import Logger

# GENERAL PYTHON PACKAGES
import numpy as np
import os
import threading
import collections  # circular buffer

# BCITP PACKAGES
from utils import save_matrix_as_NPY
from utils import load_as_matrix

import bcitp.hardware.open_bci_v3 as bci
import bcitp.hardware.open_bci_playback as playback

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'

# STANDARD BAUDRATE
BAUD = 115200


class DataHandler(threading.Thread):

    def __init__(self, p, buf_len, daisy=False, mode='openbci',
                 playback_path=None, dummy=False):
        super(DataHandler, self).__init__()

        self._stop = threading.Event()

        self.sample_counter = 0

        self.stop_flag = False

        # create a qeue for input data
        self.circ_buffer = collections.deque(
            maxlen=buf_len)

        # create a qeue for time series
        self.time_buffer = collections.deque(maxlen=buf_len)

        if mode == 'openbci':
            Logger.info('OpenBCI mode detected. Getting data from board.')
            self.board = bci.OpenBCIBoard(port=p, baud=BAUD, daisy=daisy)

        elif mode == 'simu':
            Logger.info('Simulation mode detected.')
            if self.dummy:
                Logger.info('Outputing dummy data.')
                loadedData = np.ones([2, 16])
            else:
                Logger.info('Outputing data from EEG file.')
                loadedData = load_as_matrix(self.playback_path).T

            self.board = playback.OpenBCIBoard(port=p,
                                               baud=BAUD,
                                               daisy=daisy,
                                               data=loadedData)

    def run(self):
        '''
            Gets Samples from the amplifier
        '''
        self.board.start_streaming(self.get_data)

    def store_data(self, new_data):
        '''
            Accumulates new_data in a all_data matrix
        '''

        data = np.array(new_data)  # transform list into numpy array

        if not hasattr(self, 'all_data'):
            self.all_data = np.array([]).reshape(0, len(data))

        self.all_data = np.vstack(
            (self.all_data, data))  # append to data stack

    def save_data(self, path):
        '''
            Saves the acquired EEG data into a .npy file
        '''

        save_matrix_as_NPY(self.all_data, path, mode='w')

    def get_data(self, sample):
        '''
            Get the data from amplifier and push it into the circular buffer.
            Also implements a counter to plot against the read value
            ps: This function is called by the OpenBci start_streaming()
            function
        '''

        indata = sample.channel_data
        self.update_circ_buffer(indata)
        self.store_data(indata)
        self.sample_counter += 1

        if(self.stop_flag):
            self.stop()

    def get_buffer_data(self):
        '''
            Returns the circular buffer data
        '''
        t = np.array(self.time_buffer)
        d = np.array(self.circ_buffer)

        return t, d

    def update_circ_buffer(self, data):
        '''
            Updates the samples in the circular buffer
        '''

        self.circ_buffer.append(data)
        self.time_buffer.append(self.sample_counter)

    def clear_buffer(self):
        '''
            Flushes the data inside the circular buffer
        '''
        self.circ_buffer.clear()
        self.time_buffer.clear()

    def stop(self):
        '''
            Stops the communication with the amplifier
        '''
        Logger.info('Streaming stopped. Closing connection to hardware')
        self.board.stop()
        self.board.disconnect()
        self._stop.set()

    def stopped(self):
        '''
            Checks if the DH is communicating with the amplifier
        '''
        return self._stop.isSet()
