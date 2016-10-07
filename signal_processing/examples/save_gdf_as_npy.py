import sys

sys.path.insert(1, '../')

from approach import Approach
import numpy as np

from random import randint

from DataManipulation import saveMatrixAsTxt

DATA_FOLDER_PATH = "/arquivos/Documents/eeg_data/bci_comp_IV/standard_data/"
EVENTS_FOLDER_PATH = "/arquivos/Documents/eeg_data/bci_comp_IV/standard_events/"

DATA_PATH = DATA_FOLDER_PATH + "A05E.npy"

# EVENTS INFO PATH
EVENTS_PATH = EVENTS_FOLDER_PATH + "A05E.npy"

SAMPLING_FREQ = 250.0


SAVE_PATH = '/arquivos/Documents/eeg_data/bci_comp_IV/split_datasets/split7.npy'
NEW_EVENTS_PATH = '/arquivos/Documents/eeg_data/bci_comp_IV/split_datasets/split7_events.npy'

saveMatrixAsTxt(new_data, SAVE_PATH)
saveMatrixAsTxt(new_events, NEW_EVENTS_PATH)
