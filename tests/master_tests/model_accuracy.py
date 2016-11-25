import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import sys
sys.path.insert(0, '../../')

from signal_processing.approach import Approach
from sklearn.metrics import mean_squared_error

import sys
import math
sys.path.insert(1, 'bci_ml')

import numpy as np

from random import randint

from signal_processing.DataManipulation import saveMatrixAsTxt


DATA_FOLDER_PATH = "/home/rafael/Documents/eeg_data/eeg_comp/standard_data/"
EVENTS_FOLDER_PATH = "/home/rafael/Documents/eeg_data/eeg_comp/standard_events/"

SUBJ = '1'

SAMPLING_FREQ = 250.0

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 7

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1, 2, 3, 4]

T_MIN, T_MAX = 2.5, 4.5  # time before event, time after event

CSP_N = 8

# ================ TRAIN MODEL ===========================
# ========================================================
# ========================================================

DATA_PATH = DATA_FOLDER_PATH + 'A0' + SUBJ + 'T.npy'

# EVENTS INFO PATH
EVENTS_PATH = EVENTS_FOLDER_PATH + 'A0' + SUBJ + 'T.npy'
EVENT_IDS = [1, 2]

ap2 = Approach()

ap2.defineApproach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF,
                   FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap2.setPathToCal(DATA_PATH, EVENTS_PATH)

ap2.setValidChannels(range(22))

crossvalscore, result_report, TFNP = ap2.cross_validate_model(10, 0.2)

score_label1 = np.mean(result_report[0])
score_label2 = np.mean(result_report[1])

precision_label1 = np.mean(result_report[2])
precision_label2 = np.mean(result_report[3])

autoscore = ap2.trainModel()

print('Crossvalidation Score {}'.format(crossvalscore))
# print('Class 1 Score {}'.format(score_label1))
# print('class 2 Score {}'.format(score_label2))
# print('class 1 Precision {}'.format(precision_label1))
# print('class 2 Precision {}'.format(precision_label2))

print('-----------------------------------')
print('True Negatives: {}'.format(TFNP[0]))
print('False Negatives: {}'.format(TFNP[1]))
print('True Positives: {}'.format(TFNP[2]))
print('False Positives: {}'.format(TFNP[3]))

print('-----------------------------------')
print('Positive rate: {}'.format(TFNP[0] + TFNP[1]))
print('Negative rate: {}'.format(TFNP[2] + TFNP[3]))