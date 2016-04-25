
"""CSP + LDA approach.
Implements the CSP + LDA approach using a data from the V BCI competition
"""
import mne

from data_processing import *

from mne import Epochs, pick_types, find_events
from mne.channels import read_layout
from mne.decoding import CSP

# DATASETS PATH
# data_train_path = "/arquivos/Documents/eeg_data/doutorado_cleison/data_set/A01T.set"

#data_train_path = "/arquivos/Documents/eeg_data/doutorado_cleison/A01T.gdf"
data_train_path = "/arquivos/mestrado/repo/bci_training_platform/data/data_teste/user1/samples.txt"
# filename = "/arquivos/downloads/testpport_1to100.bdf"

# EVENTS INFO PATH
#train_events_path = "/arquivos/Documents/eeg_data/doutorado_cleison/train_events/A01T.csv"

train_events_path = "/arquivos/mestrado/repo/bci_training_platform/data/data_teste/user1/marcas.txt"

# raw = mne.io.read_raw_eeglab(data_train_path)

data = loadAsMatrix(data_train_path)
data = data.T
fs = 250

data = nanCleaner(data)

ch_names = ['Fz', 'EEG1', 'EEG2', 'EEG3', 'EEG4', 'EEG5', 'EEG6', 'EEG-C3']

sfreq = fs

ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

raw = mne.io.RawArray(data, info)

events_list = readEvents(train_events_path)
dummy = range(events_list.shape[0])
events_list = np.insert(events_list, 1, dummy, axis=1) # insert new column to fit mne event format

# Processing beggining:
tmin, tmax = 0,1  # time before event, time after event
event_id = dict(LH=0, RH=1)

# Apply band-pass filter
raw.filter(8., 30., method='iir', filter_length=10)

epochs, labels = extractEpochs(raw, events, event_id, tmin, tmax)

###############################################################################
# Classification with linear discrimant analysis

from sklearn.lda import LDA  # noqa
from sklearn.cross_validation import ShuffleSplit  # noqa

# Assemble a classifier
svc = LDA()
csp = CSP(n_components=6, reg=None, log=True, cov_est='epoch')

# Define a monte-carlo cross-validation generator (reduce variance):
cv = ShuffleSplit(len(labels), 10, test_size=0.2, random_state=42)
scores = []
epochs_data = epochs.get_data()

# Use scikit-learn Pipeline with cross_val_score function
from sklearn.pipeline import Pipeline  # noqa
from sklearn.cross_validation import cross_val_score  # noqa
clf = Pipeline([('CSP', csp), ('SVC', svc)])
scores = cross_val_score(clf, epochs_data, labels, cv=cv, n_jobs=1)

# Printing the results
class_balance = np.mean(labels == labels[0])
class_balance = max(class_balance, 1. - class_balance)
print("Classification accuracy: %f / Chance level: %f" % (np.mean(scores),
                                                          class_balance))