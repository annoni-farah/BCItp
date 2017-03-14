import sys
import numpy as np

# PLOTS
import matplotlib.pyplot as plt

sys.path.insert(0, '../../..')

from bcitp.signal_processing.approach import Approach

DATA_FOLDER_PATH = "/home/rafael/repo/bcitp/data/session/mario_1/"

DATA_CAL_PATH = DATA_FOLDER_PATH + "data_cal.npy"

# EVENTS INFO PATH
CAL_EVENTS_PATH = DATA_FOLDER_PATH + "events_cal.npy"

SAMPLING_FREQ = 125.0

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1, 2]

T_MIN, T_MAX = 0, 2  # time before event, time after event

CSP_N = 10

ap = Approach()

ap.define_approach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF, FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.set_cal_path(DATA_CAL_PATH, CAL_EVENTS_PATH)

ap.set_valid_channels([-1])
# ap.define_bad_epochs(100)

autoscore = ap.train_model()

crossvalscore = ap.cross_validate_model(10, 0.2)

print autoscore
print crossvalscore

# test on single epoch

data, events = ap.load_data(DATA_CAL_PATH, CAL_EVENTS_PATH)

buf = np.array([data.shape[0], 250])

increment = 50

prob1h = []
prob2h = []
labelh = []

i = 0
tinit, tend = 0, 250

while tend < data.shape[1]:

    idx = range(tinit, tend)

    buf = data[:, idx]

    p = ap.classify_epoch(buf, out_param='prob')[0]

    prob1h.extend([p[0]])
    prob2h.extend([p[1]])
    labelh.extend([g])

    tinit += increment
    tend += increment

smooth_window = 30

smooth_prob1h = np.convolve(prob1h, np.ones((smooth_window,)) / smooth_window, mode='valid')
smooth_prob2h = np.convolve(prob2h, np.ones((smooth_window,)) / smooth_window, mode='valid')

labels_pos = events[0]
labels = events[1]

n_samples = smooth_prob1h.shape[0]

samples = range(n_samples)

plt.plot(samples, smooth_prob1h)
# plt.plot(samples, smooth_prob2h)
# plt.plot(labelh)

plt.grid(True)

# plt.fill_between([0,10000],[0.5,1])

plt.show()
