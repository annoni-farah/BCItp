# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 11:33:00 2016

@author: rafael
"""

import numpy as np # numpy - used for array and matrices operations
import math as math # used for basic mathematical operations

import scipy.signal as sp
import scipy.linalg as lg

from scipy.fftpack import fft

from pylab import plot, show, pi
import mne

from mne import Epochs, pick_types, find_events

from sklearn.lda import LDA
from mne.decoding import CSP # Import Common Spatial Patterns
from sklearn.pipeline import Pipeline
    
class DataProcessing:
    def __init__(self):
        pass

    def DesignFilter(self,fl, fh, srate, forder, filt_type = 'iir'):
        
        nyq = 0.5 * srate
        low = fl / nyq
        high = fh / nyq

        if filt_type == 'iir':
            # self.b, self.a = sp.butter(self.filter_order, [low, high], btype='band')
            self.b, self.a = sp.iirfilter(forder, [low, high], btype='band')

        elif filt_type == 'fir':
            self.b = sp.firwin(forder, [low, high], window = 'hamming',pass_zero=False)
            self.a = [1]

    def ApplyFilter(self, data_in):
    
        data_out = sp.filtfilt(self.b, self.a, data_in)

        return data_out

    def ComputeEnergy(self, data_in):

        data_squared = data_in ** 2
        # energy in each channel [e(ch1) e(ch2) ...]
        energy = np.mean(data_squared, axis = 0)

        return energy

    def GenerateWindow(self, win_len, n_seg, w_type = 'black'):
        ov = 0.5 # windows overlap

        seg_len = int(win_len / math.floor((n_seg * ov) + 1))

        print seg_len

        if w_type == 'han':
            win_seg = np.hanning(seg_len)

        if w_type == 'ham':
            win_seg = np.hamming(seg_len)

        if w_type == 'black':
            win_seg = np.blackman(seg_len)

        self.window = np.zeros(win_len)

        idx = np.array(range(seg_len))
        for i in range(n_seg):
            new_idx = idx + seg_len*ov*i
            new_idx = new_idx.astype(int)
            self.window[new_idx] = self.window[new_idx] +  win_seg

        # w[:seg_len] = w[:seg_len] + win_seg
        # w[seg_len/2: (3 *seg_len)/2 ] = w[seg_len/2: (3 *seg_len)/2 ] + win_seg
        # w[seg_len:] = w[seg_len:] + win_seg



