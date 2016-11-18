import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../')

from signal_processing.approach import Approach
from sklearn.metrics import mean_squared_error

import sys

sys.path.insert(1, 'bci_ml')

import numpy as np

from random import randint

from signal_processing.DataManipulation import saveMatrixAsTxt


DATA_FOLDER_PATH = "/home/rafael/Documents/eeg_data/eeg_comp/standard_data/"
EVENTS_FOLDER_PATH = "/home/rafael/Documents/eeg_data/eeg_comp/standard_events/"

SUBJ = '7'

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
ap2.define_bad_epochs(100)

autoscore = ap2.trainModel()

crossvalscore = ap2.cross_validate_model(10, 0.2)

print crossvalscore

# ================ GENERATE FAKE DATASET =================
# ========================================================
# ========================================================

DATA_PATH = DATA_FOLDER_PATH + 'A0' + SUBJ + 'E.npy'

# EVENTS INFO PATH
EVENTS_PATH = EVENTS_FOLDER_PATH + 'A0' + SUBJ + 'E.npy'
ap = Approach()

ap.defineApproach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF,
                  FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.setValidChannels(range(22))

data, ev = ap.loadData(DATA_PATH, EVENTS_PATH)

epochs, labels = ap.loadEpochs(data, ev)

# epochs = ap.preProcess(epochs)

idx_1 = np.where(labels == 1)[0]
idx_2 = np.where(labels == 2)[0]
idx_3 = np.where(labels == 3)[0]
idx_4 = np.where(labels == 4)[0]

# ================ APPEND EPOCHS =================

N_RUNS = 100
first = True

for a in range(N_RUNS):

    new_data_labels = np.array([0, 0])
    new_data = np.zeros([1, 22])

    for j in range(1):
        # add epochs from class 1 (left)
        for i in range(0, 6):
            k = randint(0, len(idx_1) - 1)
            # k = i
            new_data_labels = np.vstack(
                (new_data_labels, [1, int(new_data.shape[0])]))
            new_data = np.vstack((new_data, epochs[idx_1[k]].T))

    data, events = ap2.loadData(new_data, new_data_labels, data_format='npy')

    data = data.T

    buf = np.array([data.shape[0], 500])

    increment = 13

    u_time = np.array([])
    U_time = np.array([])
    U_max = 100
    U = 0
    i = 0
    tinit, tend = 0, 500

    while tend < data.shape[1]:

        idx = range(tinit, tend)

        buf = data[:, idx]

        p = ap2.applyModelOnEpoch(buf, out_param='prob')[0]
        g = ap2.applyModelOnEpoch(buf, out_param='label')

        u = p[0] - p[1]
        u_time = np.append(u_time, u)
        U = U + u

        # if abs(U) > U_max:
        #     U = 0
        U_time = np.append(U_time, U)

        tinit += increment
        tend += increment

    if first:
        u_avg = np.zeros(u_time.shape)
        U_avg = np.zeros(U_time.shape)
        u_h = np.zeros(u_time.shape)
        U_h = np.zeros(U_time.shape)
        first = False

    u_h = np.vstack([u_h, u_time])
    U_h = np.vstack([U_h, U_time])

    u_avg += u_time
    U_avg += U_time

u_avg = u_avg / float(N_RUNS)
U_avg = U_avg / float(N_RUNS)

mse_u = []
mse_U = []
for i in range(1, u_h.shape[0]):
    m_u = mean_squared_error(u_avg, u_h[i])
    m_U = mean_squared_error(U_avg, U_h[i])
    mse_u.extend([m_u])
    mse_U.extend([m_U])

idx_max_error_u = np.argmax(mse_u)

u_error = u_h[idx_max_error_u]
U_error = U_h[idx_max_error_u]


# ================ PLOT RESULTS ==========================
# ========================================================
# ========================================================

n_samples = u_time.shape[0]

time = range(n_samples)
time = [x * increment / SAMPLING_FREQ for x in time]

plt.plot()

plt.subplot(2, 1, 1)
plt.plot(time, U_avg, 'k', linewidth=4.0, label='Mean')
plt.plot(time, U_error, 'r', linewidth=.5, label='Max MSE')
plt.grid(True)
# plt.axis([0, 6, -20, 120])
# plt.axis('equal')
plt.ylabel('U')
# plt.xlabel('Time (s)')
plt.grid(True)
plt.legend(loc=0)

plt.subplot(2, 1, 2)
plt.plot(time, u_avg, 'k', linewidth=3.0, label='Mean')
plt.plot(time, u_error, 'r', linewidth=.5, label='Max MSE')
plt.grid(True)
plt.axis([0, 10, -1.2, 1.2])
# plt.axis('equal')
plt.ylabel('u')
plt.xlabel('Time (s)')
plt.grid(True)
plt.legend(loc=0)

plt.show()
