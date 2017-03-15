#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from threading import Thread
import numpy as np
import os

from math import floor
from random import randint

import threading

import collections  # circular buffer

from utils import saveMatrixAsTxt
from utils import LoadDataAsMatrix

from bcitp.signal_processing.handler import extract_epochs, read_events

from bcitp.signal_processing.processor import Filter

import bcitp.hardware.open_bci_v3 as bci
import bcitp.hardware.open_bci_playback as playback

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'

BAUD = 115200

# define a classe manager


class SampleManager(threading.Thread):

    def __init__(self, p, buf_len, daisy=False, mode='openbci',
                 path=None, labels_path=None, dummy=False):
        super(SampleManager, self).__init__()

        self._stop = threading.Event()

        self.sample_counter = 0

        self.stop_flag = False

        self.acq_mode = mode

        self.first_sample = True

        self.playback_path = path
        self.playback_labels_path = labels_path
        self.last_playback_label = [None, None]
        self.current_playback_label = [None, None]
        self.next_playback_label = [None, None]

        self.dummy = dummy

        self.buffer_length = buf_len

        self.daisy = daisy

        self.circBuff = collections.deque(
            maxlen=self.buffer_length)  # create a qeue for input data
        # create a qeue for time series
        self.tBuff = collections.deque(maxlen=self.buffer_length)

        self.event_list = np.array([]).reshape(0, 2)

        self.current_cmd = 0
        smin = int(floor(0.80 * 125))
        smax = int(floor(1.20 * 125))
        self.winning = 1

        if self.acq_mode == 'openbci':

            self.board = bci.OpenBCIBoard(port=p, baud=BAUD, daisy=self.daisy)

        elif self.acq_mode == 'simu':

            if self.dummy:
                loadedData = np.ones([2, 16])
                self.board = playback.OpenBCIBoard(
                    port=p, baud=BAUD, daisy=self.daisy, data=loadedData)

            else:
                data = LoadDataAsMatrix(self.playback_path).T[:22]
                f = Filter(8, 30, 125,
                           5, filt_type='iir', band_type='band')

                self.loadedData = f.apply_filter(data)
                if not self.playback_labels_path == '':
                    self.playback_labels = iter(
                        LoadDataAsMatrix(self.playback_labels_path))
                    self.current_playback_label = next(self.playback_labels)
                    self.next_playback_label = next(self.playback_labels)

                ev = read_events(self.playback_labels_path)
                self.epochs, self.labels = extract_epochs(
                    self.loadedData,
                    ev,
                    smin,
                    smax,
                    [1, 2])

                self.playbackData = np.zeros([1, self.epochs.shape[1]])

                self.board = playback.OpenBCIBoard(port=p,
                                                   baud=BAUD,
                                                   daisy=self.daisy,
                                                   data=self.playbackData)

                self.append_epoch()
                self.append_epoch()

    def run(self):

        # start getting data from amplifier
        self.board.start_streaming(self.GetData)

    def StoreData(self, new_data):

        data = np.array(new_data)  # transform list into numpy array

        if not hasattr(self, 'all_data'):
            self.all_data = np.array([]).reshape(0, len(data))

        self.all_data = np.vstack(
            (self.all_data, data))  # append to data stack

    def SaveData(self, path):

        saveMatrixAsTxt(self.all_data, path, mode='w')

    def GetData(self, sample):
        '''
        Get the data from amplifier and push it into the circular buffer.
        Also implements a counter to plot against the read value
        ps: This function is called by the OpenBci start_streaming() function
        '''

        indata = sample.channel_data

        if not self.expected_package(sample.id):
            pass
            # print 'wrong sequence'
            # nan_arr = np.empty(len(indata))
            # nan_arr[:] = np.nan
            # nan_arr = nan_arr.tolist()

        self.updateCircBuf(indata)
        self.StoreData(indata)

        if self.board.sample_counter > self.playbackData.shape[0] - 10:
            self.append_epoch()

        self.sample_counter += 1

        if(self.stop_flag):
            self.Stop()

    def expected_package(self, sid):

        if self.first_sample:
            self.last_sid = sid
            self.first_sample = False

        else:
            if self.daisy:
                if sid == (self.last_sid + 2) % 256:
                    self.last_sid = sid
                    return True
                else:
                    self.last_sid = sid
                    return False
            else:
                if sid == (self.last_sid + 1) % 256:
                    return True
                    self.last_sid = sid
                else:
                    return False
                    self.last_sid = sid

        # print 'sid: ', sid
        # print 'last sid: ', self.last_sid

    def GetBuffData(self, mode=None):
        t = np.array(self.tBuff)
        d = np.array(self.circBuff)

        return t, d

    def Stop(self):
        print('Streaming stopped. Closing connection to hardware')
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

        saveMatrixAsTxt(self.event_list, path, mode='w')

    def append_epoch(self):
        # print('Appending epoch: ', self.current_cmd)

        if self.current_cmd == 0:
            idx1 = np.where(self.labels == 1)[0]
            idx2 = np.where(self.labels == 2)[0]
            if self.winning == 1:
                k = randint(0, len(idx2) - 1)
                idx = idx2[k]
            else:
                k = randint(0, len(idx1) - 1)
                idx = idx1[k]

        else:
            idx12 = np.where(self.labels == self.current_cmd)[0]
            k = randint(0, len(idx12) - 1)
            idx = idx12[k]

        self.playbackData = np.vstack(
            [self.playbackData, self.epochs[idx].T])

        self.board.playback_data = self.playbackData

    def clear_buffer(self):
        self.circBuff.clear()
        self.tBuff.clear()
        # self.playbackData = np.delete(self.playbackData,
        #                               range(self.board.sample_counter + 30,
        #                                     self.playbackData.shape[0]),
        #                               axis=0)
        # self.append_epoch()

    def jump_playback_data(self):
        self.board.sample_counter = self.board.playback_data.shape[0] - 50
