import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import sys
import os
import math
from random import randint

sys.path.insert(1, os.path.join(sys.path[0], '../../..'))

from bcitp.signal_processing.approach import Approach


DATA_PATH = "/home/rafael/repo/bcitp/data/session/mario_1345/data_cal.npy"
EVENTS_PATH = "/home/rafael/repo/bcitp/data/session/mario_1345/events_cal.npy"

SAMPLING_FREQ = 125.0

N_CHANNELS = 16

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1, 2]

CSP_N = 0

crossvalscore = 0

T_MIN = 1.2
delta = 2

T_h = []
A_h = []

while CSP_N < 16:

    CSP_N = CSP_N + delta
    T_MAX = T_MIN + 2  # time before event, time after event

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
    print('Crossvalidation Score {}'.format(crossvalscore))
    print('-----------------------------------')

    T_h.extend([T_MIN])
    A_h.extend([crossvalscore])

    # print('Positive rate: {}'.format(TFNP[0] + TFNP[1]))
    # print('Negative rate: {}'.format(TFNP[2] + TFNP[3]))

    # ================ GENERATE FAKE DATASET =================
    # ========================================================
    # ========================================================


print max(A_h)
idx = A_h.index(max(A_h))
print T_h[idx]
