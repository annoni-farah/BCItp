#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BCItp
#
# Copyright (C) 2014-2017 BCItp Project
# Author: Rafael Duarte <rmendesduarte@gmail.com>
# URL: <http://bcitp.readthedocs.io/>
# For license information, see LICENSE.TXT

# KIVY PACKAGES
from kivy.logger import Logger

# GENERAL PYTHON PACKAGES
import numpy as np
import os
import threading
import collections  # circular buffer

# BCITP PACKAGES
from bcitp.utils.utils import save_matrix_as_NPY
from bcitp.utils.utils import load_as_matrix

import bcitp.hardware.open_bci_v3 as bci
import bcitp.hardware.open_bci_playback as playback

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'

# STANDARD BAUDRATE FOR OPENBCI BOARD
BAUD = 115200


class DataHandler(threading.Thread):
    '''
        A Class for handling the communication with the EEG amplifier and
        the sample management. Create as a thread to be run in parallel with
        other functions of the platform.
    '''

    def __init__(self, port, buffer_len, daisy=False, mode='openbci',
                 playback_data_path=None, dummy=False):
        super(DataHandler, self).__init__()

        self._stop = threading.Event()
        self.stop_flag = False

        # Create sample counter variable
        self.sample_counter = 0

        # Create a qeue for input data
        self.circ_buffer = collections.deque(
            maxlen=buffer_len)

        # Create a qeue for time series
        self.time_buffer = collections.deque(maxlen=buffer_len)

        # Board variables:
        self.mode = mode
        self.dummy = dummy
        self.daisy = daisy
        self.port = port

    def init_board(self):
        '''
            Initiate the acquisition board based on the mode set.
        '''

        if self.mode == 'openbci':
            Logger.info('OpenBCI mode detected. Getting data from board.')
            self.board = bci.OpenBCIBoard(
                port=self.port, baud=BAUD, daisy=self.daisy)

        elif self.mode == 'simu':
            Logger.info('Simulation mode detected.')
            if self.dummy:
                Logger.info('Outputing dummy data.')
                # Create a dummy matrix of data with value = 1
                loadedData = np.ones([2, 16])
            else:
                Logger.info('Outputing data from EEG file.')
                loadedData = load_as_matrix(self.playback_data_path).T

            self.board = playback.OpenBCIBoard(port=self.port,
                                               baud=BAUD,
                                               daisy=self.daisy,
                                               data=loadedData)

    def _store_data(self, new_data):
        '''
            Accumulates(appends) new_data in a all_data matrix.

            :param new_data: input data array
        '''

        data = np.array(new_data)  # transform list into numpy array

        if not hasattr(self, 'all_data'):
            self.all_data = np.array([]).reshape(0, len(data))

        self.all_data = np.vstack(
            (self.all_data, data))  # append to data stack

    def _get_data(self, sample):
        '''
            Get the data from amplifier and push it into the circular buffer.
            Also implements a counter to plot against the read value
            ps: This function is called by the OpenBci start_streaming()
            function
        '''

        indata = sample.channel_data
        self._update_circ_buffer(indata)
        self._store_data(indata)
        self.sample_counter += 1

        if(self.stop_flag):
            self.stop()

    def _update_circ_buffer(self, data):
        '''
            Updates the samples in the circular buffer
        '''

        self.circ_buffer.append(data)
        self.time_buffer.append(self.sample_counter)

    def run(self):
        '''
            Gets Samples from the amplifier
        '''
        self.board.start_streaming(self._get_data)

    def save_data(self, path):
        '''
            Saves the acquired EEG data into a .npy file
        '''

        save_matrix_as_NPY(self.all_data, path, mode='w')

    def get_buffer_data(self):
        '''
            Returns the circular buffer data
        '''
        t = np.array(self.time_buffer)
        d = np.array(self.circ_buffer)

        return t, d

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
