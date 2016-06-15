
import json

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
        self.sampling_freq = None

        # DATA PROCESSING SETTINGS

        self.buf_len = None
        self.channels = None
        self.f_low = None
        self.f_high = None
        self.f_order = None

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


    def getDataProcessingConfig(self):
        
        buf_len = int(self.buf_len)
        f_low = int(self.f_low)
        f_high = int(self.f_high)
        f_order = int(self.f_order)
        channels = map(int, self.channels.split(" "))

        return buf_len, f_low, f_high, f_order, channels

    def getAcquisitionConfig(self):

        mode = self.mode
        com_port = self.com_port
        baud_rate = self.baud_rate
        ch_labels = self.ch_labels
        path_to_file = self.path_to_file
        fs = self.sampling_freq


        return mode, com_port, baud_rate, ch_labels, path_to_file, fs

    def getCalibrationConfig(self):

        n_trials = int(self.n_trials)
        cue_offset = int(self.cue_offset)
        pause_offset = int(self.pause_offset)
        end_trial_offset = int(self.end_trial_offset)

        return n_trials, cue_offset, pause_offset, end_trial_offset

    def getPreCalibrationConfig(self):

        ch_left = map(int, self.pc_ch_energy_left.split(' '))
        ch_right = map(int, self.pc_ch_energy_right.split(' '))
        total_time = int(self.pc_total_time)
        relax_time = int(self.pc_relax_time)
        sign_direction = self.pc_sign_direction
        plot_flag = bool(self.pc_plot_flag)
        
        return ch_left, ch_right, total_time, relax_time, sign_direction, plot_flag

    def getMachineLearningConfig(self):

        epoch_start = float(self.ml_epoch_start)
        epoch_end = float(self.ml_epoch_end)
        method = self.ml_pp_method
        neibourghs = int(self.ml_pp_nei)
        ids = map(int, self.ml_class_ids.split(' '))
        
        return epoch_start, epoch_end, method, neibourghs, ids


    def loadFromJson(self, path):
        with open(path, "r") as data_file:    
            data = json.load(data_file)

            self.name = data["name"]
            self.date = data["date"]
            self.description = data["description"]

            # ACQUISITION SETTINGS
            self.mode = data["mode"]
            self.com_port = data["com_port"]
            self.ch_labels = data["ch_labels"]
            self.baud_rate = data["baud_rate"]
            self.path_to_file = data["path_to_file"]
            self.sampling_freq = data["sampling_freq"]

            # DATA PROCESSING SETTINGS

            self.buf_len = data["buf_len"]
            self.channels = data["channels"]
            self.f_low = data["f_low"]
            self.f_high = data["f_high"]
            self.f_order = data["f_order"]

            # PRECAL SETTINGS

            self.pc_ch_energy_left = data["pc_ch_energy_left"]
            self.pc_ch_energy_right = data["pc_ch_energy_right"]
            self.pc_total_time = data["pc_total_time"]
            self.pc_relax_time = data["pc_relax_time"]
            self.pc_sign_direction = data["pc_sign_direction"]
            self.pc_plot_flag = data["pc_plot_flag"]


            # CAL SETTINGS

            self.c_n_trials = data["c_n_trials"]
            self.c_cue_offset = data["c_cue_offset"]
            self.c_pause_offset = data["c_pause_offset"]
            self.c_end_trial_offset = data["c_end_trial_offset"]
            self.data_cal_path = data["data_cal_path"]
            self.events_cal_path = data["events_cal_path"]

            # VAL SETTINGS

            self.v_n_trials = data["v_n_trials"]
            self.v_cue_offset = data["v_cue_offset"]
            self.v_pause_offset = data["v_pause_offset"]
            self.v_end_trial_offset = data["v_end_trial_offset"]

            self.data_val_path = data["data_val_path"]
            self.events_val_path = data["events_val_path"]

            # ML SETTINGS

            self.ml_epoch_start = data["ml_epoch_start"]
            self.ml_epoch_end = data["ml_epoch_end"]
            self.ml_pp_method = data["ml_pp_method"]
            self.ml_pp_nei = data["ml_pp_nei"]
            self.ml_class_ids = data["ml_class_ids"]




