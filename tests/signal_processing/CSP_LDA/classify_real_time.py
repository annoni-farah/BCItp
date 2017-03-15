import sys
import numpy as np
from random import randint
# PLOTS
import matplotlib.pyplot as plt

sys.path.insert(0, '../../..')

from bcitp.signal_processing.approach import Approach

DATA_FOLDER_PATH = "/home/rafael/codes/bcitp/data/session/mario_7/"

DATA_CAL_PATH = DATA_FOLDER_PATH + "data_cal.npy"

# EVENTS INFO PATH
CAL_EVENTS_PATH = DATA_FOLDER_PATH + "events_cal.npy"

# DATA_FOLDER_PATH = "/home/rafael/codes/bcitp/data/session/mario_3/"

# DATA_VAL_PATH = DATA_FOLDER_PATH + "data_cal1.npy"
# # EVENTS INFO PATH
# VAL_EVENTS_PATH = DATA_FOLDER_PATH + "events_cal1.npy"

SAMPLING_FREQ = 125.0

N_CHANNELS = 16

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1, 2]

T_MIN, T_MAX = 2.5, 4.5  # time before event, time after event

CSP_N = 10

ap = Approach()

ap.define_approach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF,
                   FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.set_cal_path(DATA_CAL_PATH, CAL_EVENTS_PATH)
# ap.set_val_path(DATA_VAL_PATH, VAL_EVENTS_PATH)

ap.set_valid_channels([-1])
# ap.define_bad_epochs(100)

autoscore = ap.train_model()

crossvalscore = ap.cross_validate_model(10, 0.2)
# valscore = ap.validate_model()

print autoscore
print crossvalscore
# print valscore

# test on single epoch
# sys.exit()
# ================ GENERATE FAKE DATASET =================
# ========================================================
# ========================================================

data, ev = ap.load_data(DATA_CAL_PATH, CAL_EVENTS_PATH)

epochs, labels = ap.load_epochs(data, ev)

idx_1 = np.where(labels == 1)[0]
idx_2 = np.where(labels == 2)[0]

class_label = 1

new_data_labels = np.array([0, 0])
new_data = np.zeros([1, N_CHANNELS])

if class_label == 1:
    # if True:
    # add epochs from class 1 (left)
    for i in range(0, 100):
        k = randint(0, len(idx_1) - 1)
        new_data_labels = np.vstack(
            (new_data_labels, [1, int(new_data.shape[0])]))
        new_data = np.vstack((new_data, epochs[idx_1[k]].T))

elif class_label == 2:
    # if True:
    # add epochs from class 2 (left)
    for i in range(0, 100):
        k = randint(0, len(idx_2) - 1)
        new_data_labels = np.vstack(
            (new_data_labels, [1, int(new_data.shape[0])]))
        new_data = np.vstack((new_data, epochs[idx_2[k]].T))

data, events = ap.load_data(new_data, new_data_labels, data_format='npy')
data = data.T

print data.shape

buf = np.array([data.shape[0], (T_MAX - T_MIN) * SAMPLING_FREQ])
tinit, tend = 0, int((T_MAX - T_MIN) * SAMPLING_FREQ)

increment = 10

prob1h = []
prob2h = []
labelh = []

i = 0
while tend < data.shape[1]:

    idx = range(tinit, tend)

    buf = data[:, idx]

    p = ap.classify_epoch(buf, out_param='prob')[0]
    g = ap.classify_epoch(buf, out_param='label')[0]

    prob1h.extend([p[0]])
    prob2h.extend([p[1]])
    labelh.extend([g])

    tinit += increment
    tend += increment

smooth_window = 30

smooth_prob1h = np.convolve(prob1h, np.ones(
    (smooth_window,)) / smooth_window, mode='valid')
smooth_prob2h = np.convolve(prob2h, np.ones(
    (smooth_window,)) / smooth_window, mode='valid')

smooth_labelh = np.convolve(labelh, np.ones(
    (smooth_window,)) / smooth_window, mode='valid')

labels_pos = events[0]
labels = events[1]

n_samples = smooth_prob1h.shape[0]

samples = range(n_samples)

plt.plot(samples, smooth_prob1h, label="Class 1")
plt.plot(samples, smooth_prob2h, label="Class 2")
# plt.plot(smooth_labelh)

plt.grid(True)
plt.legend()
# plt.fill_between([0, 10000], [0.5, 1])

plt.show()

print(sum(labelh) / float(len(labelh)))
