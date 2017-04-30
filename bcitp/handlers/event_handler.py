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

from utils import save_matrix_as_NPY


class EventHandler():
    '''
        A Class for handling the recording and storing of events.
    '''

    def __init__(self):
        super(EventHandler, self).__init__()

    def mark_events(self, ev_type):
        '''
            Accumulates(appends) new events to event list. The event label
            is grouped with its time stamp

            :param ev_type: event label
        '''
        Logger.info('Marked event ' + ev_type +
                    'at sample ' + self.sample_counter)
        new = np.array([self.sample_counter, ev_type])
        self.event_list = np.vstack((self.event_list, new))

    def save_events(self, path):
        '''
            Stores the event list in the local disk

            :param path: path to saved file
        '''
        Logger.info('Saving Events at ' + path)
        save_matrix_as_NPY(self.event_list, path, mode='w')
