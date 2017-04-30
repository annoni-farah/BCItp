import sys
sys.path.insert(0, '../..')

from bcitp.signal_processing.approach import Approach

import matplotlib.pyplot as plt

import numpy as np

DATA_FOLDER_PATH = "/home/rafael/repo/bcitp/data/session/mario_4/"

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

T_MIN, T_MAX = 2., 4.  # time before event, time after event

CSP_N = 8

ap = Approach()

ap.define_approach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF, FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.set_cal_path(DATA_CAL_PATH, CAL_EVENTS_PATH)

ap.set_valid_channels(range(16))

data, events = ap.load_data(DATA_CAL_PATH, CAL_EVENTS_PATH)

data = ap.preprocess(data)

epochs, labels = ap.load_epochs(data, events)

idx_1 = np.where(labels == 1)[0]  # left hand epoch indexes
idx_2 = np.where(labels == 2)[0]  # left hand epoch indexes

c3_idx = 0
c4_idx = 2

epoch_length = epochs.shape[2]

epoch_idx = 0

# Get the epoch from epoch_idx each class and extract the desired channel:
channel_c3 = epochs[idx_1[epoch_idx], c3_idx, :]
channel_c4 = epochs[idx_1[epoch_idx], c4_idx, :]

# Create a time array with the time length of each epoch:
time = np.linspace(0, T_MAX - T_MIN, epoch_length)

plt.plot(time, channel_c3, 'k', linewidth=2)
plt.plot(time, channel_c4, 'k', color='0.5', linewidth=2)

plt.grid(True)
# plt.axis([0, UPPER_CUTOFF, 0, 150])

plt.legend(('C3', 'C4'), loc=0, shadow=True)

plt.xlabel('Time (s)')
plt.ylabel('Voltage (' + r'$\mu$'+' V)')

plt.show()
