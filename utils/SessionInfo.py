
import json

class SessionHeader:
    def __init__(self):

        # SESSION SETTINGS
        self.setSessionConfig(None, None, None)
        # ACQUISITION SETTINGS
        self.setAcquisitionConfig(None, None, None, None, None, None, None)

        # DATA PROCESSING SETTINGS
        self.setDataProcessingConfig(None, None, None, None, None, None)

        # PRECAL SETTINGS
        self.setPreCalibrationConfig(None, None, None, None, None, None)

        # CAL SETTINGS
        self.setCalibrationConfig(None, None, None, None, None, None)

        # VAL SETTINGS
        self.setValidationConfig(None, None, None, None, None, None)

        # ML SETTINGS
        self.setMachineLearningConfig(None, None, None, None, None)


    def setSessionConfig(self, n, d, desc):

        self.name = n
        self.date = d
        self.description = desc

    def getSessionConfig(self):

        return self.name, self.date, self.description

    def setDataProcessingConfig(self, bl, ch, fl, fh, fo, no):

        self.buf_len = bl
        self.channels = ch
        self.f_low = fl
        self.f_high = fh
        self.f_order = fo
        self.notch = no

    def getDataProcessingConfig(self):
        
        buf_len = int(self.buf_len)
        f_low = int(self.f_low)
        f_high = int(self.f_high)
        f_order = int(self.f_order)
        channels = map(int, self.channels.split(" "))
        notch = bool(self.notch)

        return buf_len, f_low, f_high, f_order, channels, notch

    def setAcquisitionConfig(self, m, cp, chl, br, ptf, sf, daisy):

        self.mode = m
        self.com_port = cp
        self.ch_labels = chl
        self.baud_rate = br
        self.path_to_file = ptf
        self.sampling_freq = sf
        self.daisy = daisy

    def getAcquisitionConfig(self):

        mode = self.mode
        com_port = self.com_port
        baud_rate = self.baud_rate
        ch_labels = self.ch_labels
        path_to_file = self.path_to_file
        fs = int(self.sampling_freq)
        daisy = bool(self.daisy)


        return mode, com_port, baud_rate, ch_labels, path_to_file, fs, daisy

    def setPreCalibrationConfig(self, cel, cer, tt, rt, sd, pf):

        self.pc_ch_energy_left = cel
        self.pc_ch_energy_right = cer
        self.pc_total_time = tt
        self.pc_relax_time = rt
        self.pc_sign_direction = sd
        self.pc_plot_flag = pf

    def getPreCalibrationConfig(self):

        ch_left = map(int, self.pc_ch_energy_left.split(' '))
        ch_right = map(int, self.pc_ch_energy_right.split(' '))
        total_time = int(self.pc_total_time)
        relax_time = int(self.pc_relax_time)
        sign_direction = self.pc_sign_direction
        plot_flag = bool(self.pc_plot_flag)
        
        return ch_left, ch_right, total_time, relax_time, sign_direction, plot_flag

    def setCalibrationConfig(self, nt, co, po, eto, dcp, ecp):

        self.c_n_trials = nt
        self.c_cue_offset = co
        self.c_pause_offset = po
        self.c_end_trial_offset = eto
        self.data_cal_path = dcp
        self.events_cal_path = ecp

    def getCalibrationConfig(self):

        n_trials = int(self.c_n_trials)
        cue_offset = int(self.c_cue_offset)
        pause_offset = int(self.c_pause_offset)
        end_trial_offset = int(self.c_end_trial_offset)

        return n_trials, cue_offset, pause_offset, end_trial_offset

    def setValidationConfig(self, nt, co, po, eto, dcp, ecp):

        self.v_n_trials = nt
        self.v_cue_offset = co
        self.v_pause_offset = po
        self.v_end_trial_offset = eto
        self.data_val_path = dcp
        self.events_val_path = ecp


    def getValidationConfig(self):

        n_trials = int(self.v_n_trials)
        cue_offset = int(self.v_cue_offset)
        pause_offset = int(self.v_pause_offset)
        end_trial_offset = int(self.v_end_trial_offset)

        return n_trials, cue_offset, pause_offset, end_trial_offset

    def setMachineLearningConfig(self, es, ee, ppm, ppn, cid):

        self.ml_epoch_start = es
        self.ml_epoch_end = ee
        self.ml_pp_method = ppm
        self.ml_pp_nei = ppn
        self.ml_class_ids = cid

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

            self.setSessionConfig(data["name"], data["date"], data["description"])

            # ACQUISITION SETTINGS
            self.setAcquisitionConfig(data["mode"], data["com_port"], data["ch_labels"], 
                data["baud_rate"], data["path_to_file"],data["sampling_freq"], data["daisy"])

            # DATA PROCESSING SETTINGS
            self.setDataProcessingConfig(data["buf_len"],data["channels"],data["f_low"],
                data["f_high"],data["f_order"],data["notch"])

            # PRECAL SETTINGS            
            self.setPreCalibrationConfig(data["pc_ch_energy_left"],data["pc_ch_energy_right"],
                data["pc_total_time"],data["pc_relax_time"],data["pc_sign_direction"],data["pc_plot_flag"])

            # CAL SETTINGS
            self.setCalibrationConfig(data["c_n_trials"],data["c_cue_offset"],data["c_pause_offset"],
                data["c_end_trial_offset"],data["data_cal_path"],data["events_cal_path"])

            # VAL SETTINGS
            self.setValidationConfig(data["v_n_trials"],data["v_cue_offset"],data["v_pause_offset"],
                data["v_end_trial_offset"],data["data_val_path"],data["events_val_path"])

            # ML SETTINGS
            self.setMachineLearningConfig(data["ml_epoch_start"],data["ml_epoch_end"],
                data["ml_pp_method"],data["ml_pp_nei"],data["ml_class_ids"])





