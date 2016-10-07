import sys
sys.path.insert(0, '../')

from approach import Approach

from processing_utils import computeAvgFFT, computeAvgFFTWelch

import matplotlib.pyplot as plt

import numpy as np

DATA_FOLDER_PATH = "/home/rafael/repo/bci_training_platform/data/session/A1_comp/"

DATA_CAL_PATH = DATA_FOLDER_PATH + "data_cal.npy"

# EVENTS INFO PATH
CAL_EVENTS_PATH = DATA_FOLDER_PATH + "events_cal.npy"

SAMPLING_FREQ = 250.0

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1,2] 

T_MIN, T_MAX = 2.5,4.5  # time before event, time after event

CSP_N = 12

ap = Approach()

ap.defineApproach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF, FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.setPathToCal(DATA_CAL_PATH, CAL_EVENTS_PATH)

ap.setValidChannels(range(23))

data, events = ap.loadData(DATA_CAL_PATH, CAL_EVENTS_PATH)

data = ap.preProcess(data)

c3_idx = 7
front=1
left = 6
right = 8
back = 13

d_front = 


plt.plot(f, A1_c3, '-bo')
plt.grid(True)

plt.legend(('Lhand-C4', 'Rhand-C4'), 
	loc='upper right', shadow=True)

plt.title('6 a 8 s')

plt.show()