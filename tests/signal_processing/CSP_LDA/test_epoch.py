import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import sys
import os
import math
from random import randint

sys.path.insert(1, os.path.join(sys.path[0], '../../..'))

from bcitp.signal_processing.approach import Approach

DATASET_NAME = 'mario_4'
VAL_DATASET_NAME = 'mario_4'

DATA_PATH = "/home/rafael/codes/bcitp/data/session/" + DATASET_NAME + "/data_cal.npy"
EVENTS_PATH = "/home/rafael/codes/bcitp/data/session/" + \
    DATASET_NAME + "/events_cal.npy"

SAMPLING_FREQ = 125.0

N_CHANNELS = 16

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1, 2]

T_MIN = 3.5
T_MAX = T_MIN + 2  # time before event, time after event

CSP_N = 6

# ================ TRAIN MODEL ===========================
# ========================================================
# ========================================================

ap = Approach()
ap.define_approach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF,
                   FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.set_cal_path(DATA_PATH, EVENTS_PATH)

ap.set_valid_channels(range(N_CHANNELS))

autoscore = ap.train_model()

crossvalscore = ap.cross_validate_model(10, 0.1)

print('-----------------------------------')
print('Selfvalidation Score {}'.format(autoscore))
print('Crossvalidation Score {}'.format(crossvalscore))
print('-----------------------------------')
# print('Positive rate: {}'.format(TFNP[0] + TFNP[1]))
# print('Negative rate: {}'.format(TFNP[2] + TFNP[3]))


data, ev = ap.load_data(DATA_PATH, EVENTS_PATH)
epochs, labels = ap.load_epochs(data, ev)

for i in range(epochs.shape[0]):
    label = ap.classify_epoch(epochs[i], out_param='label')
    print('Epoch:' + str(i) + '| True Label:' +
          str(labels[i]) + '| Classified Label:' + str(label))
