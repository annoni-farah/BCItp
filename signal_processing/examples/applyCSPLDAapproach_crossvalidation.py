import sys
sys.path.insert(0, '../')

from approach import Approach


DATA_FOLDER_PATH = "/home/rafael/codes/bci_training_platform/data/session/A1_comp/"

DATA_CAL_PATH = DATA_FOLDER_PATH + "data_cal.npy"

# EVENTS INFO PATH
CAL_EVENTS_PATH = DATA_FOLDER_PATH + "events_cal.npy"

SAMPLING_FREQ = 250.0

# FILTER SPEC
LOWER_CUTOFF = 8.
UPPER_CUTOFF = 30.
FILT_ORDER = 5

# EPOCH EXTRACTION CONFIG:
EVENT_IDS = [770,769]

T_MIN, T_MAX = 2,4 # time before event, time after event

CSP_N = 8

ap = Approach()

ap.defineApproach(SAMPLING_FREQ, LOWER_CUTOFF, UPPER_CUTOFF, FILT_ORDER, CSP_N, EVENT_IDS, T_MIN, T_MAX)

ap.setPathToCal(DATA_CAL_PATH, CAL_EVENTS_PATH)

ap.setValidChannels([-1])
ap.define_bad_epochs(100)


autoscore = ap.trainModel()
crossvalscore = ap.cross_validate_model(10, 0.2)

print 'SelfValidation result: ', autoscore
print 'Cross Validation result: ', crossvalscore
