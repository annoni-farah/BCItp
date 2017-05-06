# !/usr/bin/env python
# -*- coding: utf-8 -*-

# BCItp
#
# Copyright (C) 2014-2017 BCItp Project
# Author: Rafael Duarte <rmendesduarte@gmail.com>
# URL: <http://bcitp.readthedocs.io/>
# For license information, see LICENSE.TXT

import scipy.signal as sp

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline

from algorithms.CSP import CSP


class Learner:
    '''
        A class which trains the machine learning model and classifies
        new data based on the obtained model.
    '''

    def __init__(self, model=None):
        '''
            Loads a previous trained model if existent.

            :param model: previous trained sklearn format model
        '''
        self.clf = model

    def design_LDA(self):
        '''
            Initiate the linear discriminant analysis classifier
        '''
        self.svc = LDA()

    def design_CSP(self, n_comp):
        '''
            Initiate the common spatial patterns filter

            :param n_comp: number of eigenvectors to be used
                            (must be an even number)
        '''
        self.csp = CSP(n_components=n_comp, reg=None,
                       log=True, cov_est='epoch')

    def assemble_learner(self):
        '''
            Creates a sklearn pipeline to preprocess and classify data
        '''
        self.clf = Pipeline([('CSP', self.csp), ('SVC', self.svc)])

    def learn(self, train_epochs, train_labels):
        '''
            Trains the machine learning models based on the epochs and labels
            provided

            :param train_epochs: epochs numpy matrix
                                    shape[epoch, samples, channels]
            :param train_labels: labels numpy matrix shape[epoch, label]
        '''

        self.clf.fit(train_epochs, train_labels)

    def evaluate_set(self, eval_epochs, eval_labels):

        self.score = self.clf.score(eval_epochs, eval_labels)

    def cross_evaluate_set(self, eval_epochs, eval_labels,
                           n_iter=10, test_perc=0.2):

        cv = StratifiedShuffleSplit(
            n_iter, test_size=test_perc, random_state=42)

        scores = cross_val_score(
            self.clf, eval_epochs, eval_labels, cv=cv,
            scoring=make_scorer(self.my_score))

        return scores.mean()

    def evaluate_epoch(self, epoch, out_param='label'):

        if out_param == 'prob':

            guess = self.clf.predict_proba(epoch)

        elif out_param == 'label':

            guess = self.clf.predict(epoch)

        return guess

    def get_results(self):
        return self.score

    def get_model(self):
        return self.clf


class Filter:

    def __init__(self, low_freq, high_freq, srate, forder):

        nyq = 0.5 * srate
        low = low_freq / nyq
        high = high_freq / nyq

        self.b, self.a = sp.iirfilter(forder, [low, high],
                                      btype='band')

    def apply_filter(self, data_in):

        data_out = sp.filtfilt(self.b, self.a, data_in)

        return data_out
