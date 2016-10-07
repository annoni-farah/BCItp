import sys
sys.path.insert(0, '../')

from approach import Approach


DATA_FOLDER_PATH = "/home/rafael/Documents/eeg_data/eeg_comp/125hz/standard_data/"

EVENTS_FOLDER_PATH = "/home/rafael/Documents/eeg_data/eeg_comp/125hz/standard_events/"

CHANNEL_LIST = [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21]

SAMPLING_FREQ = 125.0

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [1, 2]

T_MIN, T_MAX = 2.5, 4.5  # time before event, time after event

CSP_N = 8

for i in range(1, 2):
    print 'evaluating dataset: ', i
    dsname = 'A0' + str(i) + 'T_openbci.npy'
    DATA_CAL_PATH = DATA_FOLDER_PATH + dsname
    CAL_EVENTS_PATH = EVENTS_FOLDER_PATH + dsname

    ap = Approach()

    ap.defineApproach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF,
                      FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

    ap.setPathToCal(DATA_CAL_PATH, CAL_EVENTS_PATH)

    ap.setValidChannels([-1])
    ap.define_bad_epochs(100)

    autoscore = ap.trainModel()
    crossvalscore = ap.cross_validate_model(10, 0.2)

    # print 'SelfValidation result: ', autoscore
    print 'Cross Validation result: ', crossvalscore
