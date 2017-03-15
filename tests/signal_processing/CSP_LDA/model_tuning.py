import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import sys
import os
import math
from random import randint

sys.path.insert(1, os.path.join(sys.path[0], '../../..'))

from bcitp.signal_processing.approach import Approach


DATA_PATH = "/home/rafael/codes/bcitp/data/session/mario_4/data_cal.npy"
EVENTS_PATH = "/home/rafael/codes/bcitp/data/session/mario_4/events_cal.npy"

VAL_DATA_PATH = "/home/rafael/codes/bcitp/data/session/mario_4/data_cal.npy"
VAL_EVENTS_PATH = "/home/rafael/codes/bcitp/data/session/mario_4/events_cal.npy"

SAMPLING_FREQ = 125.0

N_CHANNELS = 16

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1, 2]

CSP_N = 8

crossvalscore = 0

T_MIN = 0
delta = 0.05

T_h = []
A_h = []

while T_MIN < 4:

    T_MIN = T_MIN + delta
    T_MAX = T_MIN + 2  # time before event, time after event

    # ================ TRAIN MODEL ===========================
    # ========================================================
    # ========================================================

    ap = Approach()
    ap.define_approach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF,
                       FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

    ap.set_cal_path(DATA_PATH, EVENTS_PATH)

    ap.set_val_path(VAL_DATA_PATH, VAL_EVENTS_PATH)

    ap.set_valid_channels(range(N_CHANNELS))

    autoscore = ap.train_model()

    crossvalscore = ap.cross_validate_model(10, 0.1)

    valscore = ap.validate_model()

    print('-----------------------------------')
    print('Crossvalidation Score {}'.format(autoscore))
    print('Crossvalidation Score {}'.format(crossvalscore))
    print('Validation Score {}'.format(valscore))
    print('-----------------------------------')

    T_h.extend([T_MIN])
    A_h.extend([autoscore])

    # print('Positive rate: {}'.format(TFNP[0] + TFNP[1]))
    # print('Negative rate: {}'.format(TFNP[2] + TFNP[3]))

    # ================ GENERATE FAKE DATASET =================
    # ========================================================
    # ========================================================


print max(A_h)
idx=A_h.index(max(A_h))
print T_h[idx]
