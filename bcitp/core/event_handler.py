#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from threading import Thread
import numpy as np


from utils import save_matrix_as_NPY


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

        save_matrix_as_NPY(self.event_list, path, mode='w')

    def clear_buffer(self):
        self.circBuff.clear()
        self.tBuff.clear()
