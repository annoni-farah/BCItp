
"""CSP + LDA approach.
Implements the CSP + LDA approach using a data from the V BCI competition
"""
# Force variables to be reseted at every run
from IPython import get_ipython
get_ipython().magic('reset -sf')

import mne

from data_processing import *

from mne.channels import read_layout
from mne.decoding import CSP

import numpy as np

subj = 3

# DATASETS PATH
data_train_path = "/arquivos/mestrado/repo/bci_training_platform/" \
                    "data/data_teste/user" + str(subj) + "/samples.txt"
train_events_path = "/arquivos/mestrado/repo/bci_training_platform/" \
                    "data/data_teste/user" + str(subj) + "/marcas.txt"

data_eval_path = "/arquivos/mestrado/repo/bci_training_platform/" \
                    "data/data_teste/user" + str(subj) + "/samples.txt"
eval_events_path = "/arquivos/mestrado/repo/bci_training_platform/" \
                    "data/data_teste/user" + str(subj) + "/marcas.txt"
tmin, tmax = 0, 1  # time before event, time after event
fmin, fmax, order = 8, 30, 10 # band pass filter specs

event_id = dict(LH=0, RH=1)
fs = 250

ch_names = ['Fz', 'EEG1', 'EEG2', 'EEG3', 'EEG4', 'EEG5', 'EEG6', 'EEG-C3']

sfreq = fs

ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']


###############################################################################
data = loadAsMatrix(data_train_path)
data = data.T
data = nanCleaner(data)

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

raw = mne.io.RawArray(data, info)

events_list = readEvents(train_events_path)
dummy = range(events_list.shape[0])
events = np.insert(events_list, 1, dummy, axis=1) # insert new column to fit mne event format

# Processing beggining:
# Apply band-pass filter
raw.filter(fmin, fmax, method='iir', filter_length=order)

epochs_train, labels_train = extractEpochs(raw, events, event_id, tmin, tmax)

###############################################################################
# Repeat the same steps for validation data:
del raw, data # clear previous data

data = loadAsMatrix(data_eval_path)
data = data.T
data = nanCleaner(data)

raw = mne.io.RawArray(data, info)

events_list = readEvents(eval_events_path)
dummy = range(events_list.shape[0])
events = np.insert(events_list, 1, dummy, axis=1) # insert new column to fit mne event format

# Apply band-pass filter
raw.filter(fmin, fmax, method='iir', filter_length=order)

epochs_eval, labels_eval = extractEpochs(raw, events, event_id, tmin, tmax)

###############################################################################
# Classification with linear discrimant analysis
ncomp = 6 # number of CSP components (must be even number)

clf, W_csp, W_lda = calcCSPLDA(epochs_train, labels_train, ncomp) 

# Extract data from mne.Epochs
epochs_data_eval = epochs_eval.get_data()

score = clf.score(epochs_data_eval, labels_eval)

# Printing the results
class_balance = np.mean(labels_eval == labels_eval[0])
class_balance = max(class_balance, 1. - class_balance)
print("Classification accuracy: %f / Chance level: %f" % (score,
                                                          class_balance))