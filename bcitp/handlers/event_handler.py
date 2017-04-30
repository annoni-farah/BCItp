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

import numpy as np

# BCITP PACKAGES
from utils.utils import save_matrix_as_NPY


class EventHandler():
    '''
        A Class for handling the recording and storing of events.
    '''

    def __init__(self):
        self.event_list = np.array([]).reshape(0, 2)

    def mark_events(self, sample_stamp, ev_type):
        '''
            Accumulates(appends) new events to event list. The event label
            is grouped with its sample time stamp

            :param sample_stamp: time stamp in sample counts
            :param ev_type: event label
        '''
        Logger.info('Marked event ' + str(ev_type) +
                    'at sample ' + str(sample_stamp))
        new = np.array([sample_stamp, ev_type])
        self.event_list = np.vstack((self.event_list, new))

    def save_events(self, path):
        '''
            Stores the event list in the local disk

            :param path: path to saved file
        '''
        Logger.info('Saving Events at ' + path)
        save_matrix_as_NPY(self.event_list, path, mode='w')

    def clear_events(self):
        '''
            Erases the current event list and creates a new empty one

        '''
        self.event_list = np.array([]).reshape(0, 2)
