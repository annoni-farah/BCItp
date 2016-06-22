
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
        self.sample_rate = None
        self.daisy = None

        # DATA PROCESSING SETTINGS
        self.buf_len = None
        self.channels = None
        self.f_low = None
        self.f_high = None
        self.f_order = None
        self.notch = None

        # PRECAL SETTINGS
        self.pc_ch_energy_left = None
        self.pc_ch_energy_right = None
        self.pc_total_time = None
        self.pc_relax_time = None
        self.pc_sign_direction = None
        self.pc_plot_flag = None

        # CAL SETTINGS
        self.c_n_trials = None
        self.c_cue_offset = None
        self.c_pause_offset = None
        self.c_end_trial_offset = None
        self.data_cal_path = None
        self.events_cal_path = None

        # VAL SETTINGS
        self.v_n_trials = None
        self.v_cue_offset = None
        self.v_pause_offset = None
        self.v_end_trial_offset = None
        self.data_val_path = None
        self.events_val_path = None

        # ML SETTINGS
        self.ml_epoch_start = None
        self.ml_epoch_end = None
        self.ml_pp_method = None
        self.ml_pp_nei = None
        self.ml_class_ids = None

    def saveToPkl(self):
        path = PATH_TO_SESSION + self.name + '/' + 'session_info.pkl'
        
        with open(path, 'w') as file_name:
            pickle.dump(self.__dict__, file_name)


    def loadFromPkl(self):
        path = PATH_TO_SESSION + self.name + '/' + 'session_info.pkl'

        with open(path, 'r') as file_name:
            load_obj = pickle.load(file_name)

        self.__dict__.update(load_obj) 





