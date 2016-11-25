# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 11:33:00 2016

@author: rafael
"""

import os
import sys
import inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split
                                                              (inspect.getfile(inspect.currentframe()))[0], 'algorithms')))

if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import numpy as np  # numpy - used for array and matrices operations
import math as math  # used for basic mathematical operations

import scipy.signal as sp
import scipy.linalg as lg

from scipy.fftpack import fft

from math import pi

# from mne import Epochs, pick_types, find_events

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import classification_report, make_scorer, accuracy_score
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

from sklearn.model_selection import ShuffleSplit, StratifiedShuffleSplit

# from mne.decoding import CSP # Import Common Spatial Patterns
from sklearn.pipeline import Pipeline

from CommonSpatialPatterns import CSP


class Learner:

    def __init__(self, model=None):
        # Loads a previous model if existent
        self.clf = model
        self.report = np.zeros([1, 4])
        self.TFNP_rate = np.array([0, 0, 0, 0])
        self.cv_counter = 0

    def DesignLDA(self):
        self.svc = LDA()

    def DesignCSP(self, n_comp):
        self.csp = CSP(n_components=n_comp, reg=None,
                       log=True, cov_est='epoch')

    def AssembleLearner(self):
        self.clf = Pipeline([('CSP', self.csp), ('SVC', self.svc)])

    def Learn(self, train_epochs, train_labels):

        self.clf.fit(train_epochs, train_labels)

    def EvaluateSet(self, eval_epochs, eval_labels):

        self.score = self.clf.score(eval_epochs, eval_labels)

        guess = self.clf.predict(eval_epochs)

        idx1 = np.where(eval_labels == 1)[0]
        accuracy1 = accuracy_score(eval_labels[idx1], guess[idx1])

        # print('Validation Score class 1 {}'.format(accuracy1))

        # report = classification_report(eval_labels, guess)

        # print(report)

    def my_score(self, y_true, y_pred):
        # score_report = classification_report(y_true, y_pred)
        # print(score_report)

        idx1 = np.where(y_true == 1)[0]
        idx2 = np.where(y_true == 2)[0]

        # precision, recall, fscore, support = precision_recall_fscore_support(
        #     y_true[idx1], y_pred[idx1])
        # print('precision:', precision.mean())

        CM = confusion_matrix(y_true[idx1], y_pred[idx1])

        # print(y_true[idx1])
        # print(y_pred[idx1])

        # print(CM)
        TN = CM[0, 0]
        FN = CM[1, 0]
        TP = CM[1, 1]
        FP = CM[0, 1]

        # print(TN)
        # print(FP)

        total = float(len(y_true[idx1]))
        # print(total)
        # print(float(TN))
        # print(float(TN) / total)
        TN_rate = float(TN) / total
        FN_rate = float(FN) / total
        TP_rate = float(TP) / total
        FP_rate = float(FP) / total

        self.TFNP_rate = np.vstack(
            [self.TFNP_rate, [TN_rate, FN_rate, TP_rate, FP_rate]])
        # print('True Negatives: {}'.format(TN))
        # print('False Negatives: {}'.format(FN))
        # print('True Positives: {}'.format(TP))
        # print('False Positives: {}'.format(FP))
        # print('-----------------------------------')
        # print(self.TFNP_rate)
        # accuracy1 = accuracy_score(y_true[idx1], y_pred[idx1])
        # accuracy2 = accuracy_score(y_true[idx2], y_pred[idx2])

        # self.report = np.vstack([self.report, [accuracy1, accuracy2,
        #                                        precision[0], precision[1]]])

        # print 'Accuracy for class 1', accuracy1
        # print 'Accuracy for class 2', accuracy2

        global_accuracy = accuracy_score(y_true[idx1], y_pred[idx1])
        self.cv_counter += 1

        # print('--------------------')

        return global_accuracy

    def cross_evaluate_set(self, eval_epochs, eval_labels, n_iter=10, test_perc=0.2):

        # cv = ShuffleSplit(n_iter, test_size=test_perc, random_state=42)
        cv = StratifiedShuffleSplit(
            n_iter, test_size=test_perc, random_state=42)

        # scorer = make_scorer(classification_report)

        scores = cross_val_score(
            self.clf, eval_epochs, eval_labels, cv=cv, scoring=make_scorer(self.my_score))

        # predicted = cross_val_predict(
        #     self.clf, eval_epochs, eval_labels, cv=10)

        return scores.mean()

    def EvaluateEpoch(self, epoch, out_param='label'):

        if out_param == 'prob':

            guess = self.clf.predict_proba(epoch)

        elif out_param == 'label':

            guess = self.clf.predict(epoch)

        return guess

    def PrintResults(self):
        # class_balance = np.mean(labels == labels[0])
        # class_balance = max(class_balance, 1. - class_balance)
        class_balance = 0.5
        print("Classification accuracy: %f / Chance level: %f" % (self.score,
                                                                  class_balance))

    def GetResults(self):
        return self.score

    def GetModel(self):
        return self.clf


class Filter:

    def __init__(self, fl, fh, srate, forder, filt_type='iir', band_type='band'):

        nyq = 0.5 * srate
        low = fl / nyq
        high = fh / nyq

        if filt_type == 'iir':
            # self.b, self.a = sp.butter(self.filter_order, [low, high],
            # btype='band')
            self.b, self.a = sp.iirfilter(forder, [low, high], btype=band_type)

        elif filt_type == 'fir':
            self.b = sp.firwin(forder, [low, high],
                               window='hamming', pass_zero=False)
            self.a = [1]

    def ApplyFilter(self, data_in):

        data_out = sp.filtfilt(self.b, self.a, data_in)

        return data_out
