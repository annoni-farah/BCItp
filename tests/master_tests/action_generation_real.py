import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../')

from signal_processing.approach import Approach


DATA_FOLDER_PATH = "/home/rafael/Documents/eeg_data/eeg_comp/standard_data/"

DATA_CAL_PATH = DATA_FOLDER_PATH + "A04T.npy"

# EVENTS INFO PATH
CAL_EVENTS_PATH = "/home/rafael/Documents/eeg_data/eeg_comp/standard_events/A04T.npy"

SAMPLING_FREQ = 250.0

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1, 2]

T_MIN, T_MAX = 2.5, 4.5  # time before event, time after event

CSP_N = 8

ap = Approach()

ap.defineApproach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF,
                  FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.setPathToCal(DATA_CAL_PATH, CAL_EVENTS_PATH)

ap.setValidChannels(range(22))
ap.define_bad_epochs(100)

autoscore = ap.trainModel()

crossvalscore = ap.cross_validate_model(10, 0.2)

print crossvalscore

# test on single epoch
DATA_FOLDER_PATH = "/home/rafael/Documents/eeg_data/eeg_comp/split_datasets/"
DATA_CAL_PATH = DATA_FOLDER_PATH + "split2.npy"
# EVENTS INFO PATH
CAL_EVENTS_PATH = DATA_FOLDER_PATH + "split2_labels.npy"

data, events = ap.loadData(DATA_CAL_PATH, CAL_EVENTS_PATH)

# data = data.T

buf = np.array([data.shape[0], 500])

increment = 13

u_time = np.array([])
U_time = np.array([])
U_max = 100

labelh = []

U = 0
i = 0
tinit, tend = 0, 500

while tend < data.shape[1]:

    idx = range(tinit, tend)

    buf = data[:, idx]

    p = ap.applyModelOnEpoch(buf, out_param='prob')[0]
    g = ap.applyModelOnEpoch(buf, out_param='label')

    u = p[0] - p[1]
    u_time = np.append(u_time, u)
    U = U + u

    if abs(U) > U_max:
        U = 0
    U_time = np.append(U_time, U)
    labelh.extend([g])

    tinit += increment
    tend += increment

# smooth_window = 30

# smooth_prob1h = np.convolve(prob1h, np.ones(
#     (smooth_window,)) / smooth_window, mode='valid')

labels_pos = events[0]
labels = events[1]

n_samples = u_time.shape[0]

time = range(n_samples)
time = [x * increment / SAMPLING_FREQ for x in time]

plt.plot()

plt.subplot(2, 1, 1)
plt.plot(time, U_time, 'k', linewidth=4.0)
plt.grid(True)
# plt.axis([0, 6, -20, 120])
# plt.axis('equal')
plt.ylabel('U')
# plt.xlabel('Time (s)')
plt.grid(True)
# plt.legend(loc=0)

plt.subplot(2, 1, 2)
plt.plot(time, u_time, 'k', linewidth=2.0)
plt.grid(True)
# plt.axis([0, 6, 0, 1.2])
# plt.axis('equal')
plt.ylabel('u')
plt.xlabel('Time (s)')
plt.grid(True)

plt.show()
