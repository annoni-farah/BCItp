
import pickle
from standards import PATH_TO_SESSION


class SessionHeader:

    def __init__(self):

        self.info = InfoHeader()
        self.acq = AcquisitionHeader()
        self.dp = DataProcessingHeader()
        self.precal = PreCalHeader()
        self.cal = CalHeader()
        self.ml = MLHeader()
        self.game = GameHeader()

    def saveToPkl(self):
        path = PATH_TO_SESSION + self.info.name + '/' + 'session_info.pkl'

        with open(path, 'w') as file_name:
            pickle.dump(self.__dict__, file_name)

    def loadFromPkl(self):
        path = PATH_TO_SESSION + self.info.name + '/' + 'session_info.pkl'

        with open(path, 'r') as file_name:
            load_obj = pickle.load(file_name)

        self.__dict__.update(load_obj)


class InfoHeader():

    def __init__(self):
        # SESSION SETTINGS
        self.flag = False

        self.name = None
        self.date = None
        self.description = None


class AcquisitionHeader():

    def __init__(self):
        # ACQUISITION SETTINGS
        self.flag = False

        self.mode = None
        self.com_port = None
        self.ch_labels = None
        self.path_to_file = None
        self.path_to_labels_file = None
        self.sample_rate = None
        self.daisy = None
        self.dummy = None


class DataProcessingHeader():

    def __init__(self):
        # DATA PROCESSING SETTINGS
        self.flag = False

        self.buf_len = None
        self.channels = None
        self.f_low = None
        self.f_high = None
        self.f_order = None
        self.notch = None


class PreCalHeader():

    def __init__(self):
        # PRECAL SETTINGS
        self.flag = False

        self.ch_energy_left = None
        self.ch_energy_right = None
        self.total_time = None
        self.relax_time = None
        self.sign_direction = None
        self.plot_flag = None


class CalHeader():

    def __init__(self):
        # CAL SETTINGS
        self.flag = False

        self.n_trials = None
        self.cue_offset = None
        self.pause_offset = None
        self.end_trial_offset = None
        self.data_cal_path = None
        self.events_cal_path = None
        self.data_val_path = None
        self.events_val_path = None

        self.n_runs = None
        self.runs_interval = None


class MLHeader():

    def __init__(self):
        # ML SETTINGS
        self.flag = False

        self.epoch_start = None
        self.epoch_end = None
        self.method = None

        self.max_amp = None
        self.max_mse = None

        self.nei = None
        self.class_ids = None

        self.n_iter = None
        self.test_perc = None


class GameHeader():

    def __init__(self):
        # GAME SETTINGS
        self.flag = False

        self.game_threshold = None
        self.window_overlap = None
        self.warning_threshold = None
        self.forward_speed = None
        self.inst_prob = None
        self.keyb_enable = None

        self.action_cmd1 = None
        self.action_cmd2 = None
