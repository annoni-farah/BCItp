import sys

sys.path.insert(1, '../')

from approach import Approach
import numpy as np

from random import randint

from DataManipulation import saveMatrixAsTxt

DATA_FOLDER_PATH = "/home/rafael/codes/bci_training_platform/data/session/A1_comp/"
EVENTS_FOLDER_PATH = "/home/rafael/codes/bci_training_platform/data/session/A1_comp/"

DATA_PATH = DATA_FOLDER_PATH + "data_cal.npy"

# EVENTS INFO PATH
EVENTS_PATH = EVENTS_FOLDER_PATH + "events_cal.npy"

SAMPLING_FREQ = 250.0

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 7

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [769, 770, 771, 772]

T_MIN, T_MAX = 0.5, 2.5  # time before event, time after event

CSP_N = 8

ap = Approach()
ap.defineApproach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF,
                  FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.setValidChannels(range(22))

data, ev = ap.loadData(DATA_PATH, EVENTS_PATH)

epochs, labels = ap.loadEpochs(data, ev)

epochs = ap.preProcess(epochs)


idx_left = np.where(labels == EVENT_IDS[0])[0]
idx_right = np.where(labels == EVENT_IDS[1])[0]
idx_foot = np.where(labels == EVENT_IDS[2])[0]
idx_tongue = np.where(labels == EVENT_IDS[3])[0]


new_data = np.zeros([1, epochs.shape[1]])
new_events = np.zeros([1, 2])

idx1 = idx_right
idx2 = idx_tongue

label1 = labels[idx1[0]]
label2 = labels[idx2[0]]


for i in range(10):
    k = randint(0, len(idx1))
    new_events = np.vstack([new_events, [new_data.shape[0], label1]])
    new_data = np.vstack([new_data, epochs[idx1[i]].T])

for i in range(40):
    k = randint(0, len(idx2))
    new_events = np.vstack([new_events, [new_data.shape[0], label2]])
    new_data = np.vstack([new_data, epochs[idx2[i]].T])

new_data = np.delete(new_data, 0, axis=0)
new_events = np.delete(new_events, 0, axis=0)

SAVE_PATH = '/media/rafael/a8062025-4bf2-4357-aa0a-553348489b90/home/rafael/eeg_data/compIV/split_datasets\
/split1.npy'

NEW_EVENTS_PATH = '/media/rafael/a8062025-4bf2-4357-aa0a-553348489b90/home/rafael/eeg_data/compIV/split_datasets\
/split1_events.npy'

saveMatrixAsTxt(new_data, SAVE_PATH)
saveMatrixAsTxt(new_events, NEW_EVENTS_PATH)
