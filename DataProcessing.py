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
    def __init__(self,fl, fh, srate, forder):
        
        self.f_low = fl
        self.f_high = fh
        self.fs = srate
        self.filter_order = forder
        self.DesignFilter()
        

    def calcCSPLDA(epochs_train, labels_train, nb):
        """Creates the CSP+LDA pipeline and applies it to training data. 
        (just really a function to call the MNE and SKlearn processing functs)

        Parameters
        ----------
        epochs_train : epochs in mne data format

        labels_train : labels of epochs in mne format

        nb: number of CSP components, must be even. (6 implies the 3 top-most and bottom eigenvectors)

        Returns
        -------
        clf : the fitted model for the CSP+LDA approach

        csp.filters_ : CSP weight vector, shape (nchannels, nchannels)

        svc.coef_ : LDA weight vector, shape (1, nb)

        Examples
        --------
        >>> data_path = "/PATH/TO/FILE/somematrix.txt"
        >>> matrix_data = loadAsMatrix(data_path)
        """
        svc = LDA()
        csp = CSP(n_components=4, reg=None, log=True, cov_est='epoch')
        clf = Pipeline([('CSP', csp), ('SVC', svc)])

        epochs_data = epochs_train.get_data()

        clf.fit(epochs_data, labels_train)

        return clf, csp.filters_, svc.coef_


    def DesignFilter(self, filt_type = 'iir'):
        
        nyq = 0.5 * self.fs
        low = self.f_low / nyq
        high = self.f_high / nyq

        if filt_type == 'iir':
            # self.b, self.a = sp.butter(self.filter_order, [low, high], btype='band')
            self.b, self.a = sp.iirfilter(self.filter_order, [low, high], btype='band')

        elif filt_type == 'fir':
            self.b = sp.firwin(self.filter_order, [low, high], window = 'hamming',pass_zero=False)
            self.a = [1]


    def ApplyFilter(self, data_in):
    
        data_out = sp.filtfilt(self.b, self.a, data_in)

        return data_out

    def ComputeEnergy(self, data_in):

        data_squared = data_in ** 2
        # energy in each channel [e(ch1) e(ch2) ...]
        energy = np.mean(data_squared, axis = 0)

        return energy