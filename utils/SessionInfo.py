from kivy.properties import ObjectProperty


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

        return mode, com_port, baud_rate, ch_labels, path_to_file

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




