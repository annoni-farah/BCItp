import sys
sys.path.insert(0, '../..')

from bcitp.signal_processing.approach import Approach

from bcitp.signal_processing.utils import computeAvgFFT, computeAvgFFTWelch

import matplotlib.pyplot as plt

import numpy as np

DATA_FOLDER_PATH = "/home/rafael/codes/bcitp/data/session/mario_6/"

DATA_CAL_PATH = DATA_FOLDER_PATH + "data_cal.npy"

# EVENTS INFO PATH
CAL_EVENTS_PATH = DATA_FOLDER_PATH + "events_cal.npy"

SAMPLING_FREQ = 125.0

# FILTER SPEC
LOWER_CUTOFF = 0.5
UPPER_CUTOFF = 50.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1, 2]

T_MIN, T_MAX = 2.6, 4.6  # time before event, time after event

CSP_N = 6

ap = Approach()

ap.define_approach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF, FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.set_cal_path(DATA_CAL_PATH, CAL_EVENTS_PATH)

ap.set_valid_channels(range(16))

data, events = ap.load_data(DATA_CAL_PATH, CAL_EVENTS_PATH)

data = ap.preprocess(data)

# nch = data.shape[0]
# Id = np.identity(nch)
# W = Id - (1.0 / nch) * np.dot(Id, Id.T)
# data = np.dot(W, data)

epochs, labels = ap.load_epochs(data, events)

idx_1 = np.where(labels == 1)[0]
idx_2 = np.where(labels == 2)[0]

c3_idx = 0
c4_idx = 2

f, A1_c3 = computeAvgFFTWelch(epochs, c3_idx, SAMPLING_FREQ, idx_1)
f, A2_c3 = computeAvgFFTWelch(epochs, c3_idx, SAMPLING_FREQ, idx_2)

# f, A1_c3 = computeAvgFFT(epochs, c3_idx, SAMPLING_FREQ, idx_1)
# f, A2_c3 = computeAvgFFT(epochs, c3_idx, SAMPLING_FREQ, idx_2)

f, A1_c4 = computeAvgFFTWelch(epochs, c4_idx, SAMPLING_FREQ, idx_1)
f, A2_c4 = computeAvgFFTWelch(epochs, c4_idx, SAMPLING_FREQ, idx_2)

f = f * SAMPLING_FREQ

plt.plot(f, A1_c3, 'k', linewidth=4)
plt.plot(f, A2_c3, 'k', color='0.5', linewidth=4)
# plt.plot(f, A2_c3, '-gs')
# plt.plot(f, A2_c4, '-gs')
plt.grid(True)
plt.axis([0, 30, 0, 50])

plt.legend(('Left Hand-C3', 'Right Hand-C3'),
           loc='upper right', shadow=True)

plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

plt.show()
