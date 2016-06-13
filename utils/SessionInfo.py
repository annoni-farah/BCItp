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

        # VAL SETTINGS

        self.v_n_trials = None
        self.v_cue_offset = None
        self.v_pause_offset = None
        self.v_end_trial_offset = None





