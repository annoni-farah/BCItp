
import pickle
from standards import *

class SessionHeader:
    def __init__(self):

        # SESSION SETTINGS
        self.name = None
        self.date = None
        self.description = None

        # ACQUISITION SETTINGS
        self.mode = None
        self.com_port = None
        self.ch_labels = None
        self.baud_rate = None
        self.path_to_file = None
        self.path_to_labels_file = None
        self.sample_rate = None
        self.daisy = None
        self.dummy = None

        # DATA PROCESSING SETTINGS
        self.buf_len = None
        self.channels = None
        self.f_low = None
        self.f_high = None
        self.f_order = None
        self.notch = None

        # PRECAL SETTINGS
        self.ch_energy_left = None
        self.ch_energy_right = None
        self.total_time = None
        self.relax_time = None
        self.sign_direction = None
        self.plot_flag = None

        # CAL SETTINGS
        self.n_trials = None
        self.cue_offset = None
        self.pause_offset = None
        self.end_trial_offset = None
        self.data_cal_path = None
        self.events_cal_path = None

        # ML SETTINGS
        self.epoch_start = None
        self.epoch_end = None
        self.method = None
        self.nei = None
        self.class_ids = None

        # GAME SETTINGS
        self.game_threshold = None
        self.window_overlap = None
        self.warning_threshold = None
        self.forward_speed = None
        self.inst_prob = None
        self.keyb_enable = None


    def saveToPkl(self):
        path = PATH_TO_SESSION + self.name + '/' + 'session_info.pkl'
        
        with open(path, 'w') as file_name:
            pickle.dump(self.__dict__, file_name)


    def loadFromPkl(self):
        path = PATH_TO_SESSION + self.name + '/' + 'session_info.pkl'

        with open(path, 'r') as file_name:
            load_obj = pickle.load(file_name)

        self.__dict__.update(load_obj) 





