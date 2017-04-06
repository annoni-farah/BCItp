#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from threading import Thread
import numpy as np
import os


from utils import saveMatrixAsTxt

GLOBALPATH = os.path.abspath(os.path.dirname(__file__))
PATHTOUSERS = GLOBALPATH + '/data/users/'


class EventHandler():

    def __init__(self):
        super(EventHandler, self).__init__()

    def StoreEvents(self, new_data):

        data = np.array(new_data)  # transform list into numpy array

        if not hasattr(self, 'all_data'):
            self.all_data = np.array([]).reshape(0, len(data))

        self.all_data = np.vstack(
            (self.all_data, data))  # append to data stack

    def MarkEvents(self, ev_type):

        new = np.array([self.sample_counter, ev_type])
        self.event_list = np.vstack((self.event_list, new))

    def SaveEvents(self, path):

        saveMatrixAsTxt(self.event_list, path, mode='w')

    def clear_buffer(self):
        self.circBuff.clear()
        self.tBuff.clear()
