############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty, \
                            ListProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

# KV file:
Builder.load_file('screens/settings/calsettings.kv')

# Generic:

# Project's:
from SampleManager import *
from standards import *
######################################################################

class CalSettings(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (CalSettings, self).__init__(**kwargs)
        
        self.sh = session_header

    def change_to_cal(self,*args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'right'

    def save_config(self,*args):

        ids = self.ids

        self.sh.cal.n_trials = ids.n_trials.value
        self.sh.cal.cue_offset = ids.cue_offset.value
        self.sh.cal.cue_time = ids.cue_time.value
        self.sh.cal.pause_offset = ids.pause_offset.value
        self.sh.cal.end_trial_offset = ids.end_trial_offset.value

        self.sh.cal.n_runs = ids.n_runs.value
        self.sh.cal.runs_interval = ids.runs_interval.value

        self.sh.cal.data_cal_path = PATH_TO_SESSION + self.sh.info.name + '/' + 'data_cal.npy'
        self.sh.cal.events_cal_path = PATH_TO_SESSION + self.sh.info.name + '/' + 'events_cal.npy'
        self.sh.cal.data_val_path = PATH_TO_SESSION + self.sh.info.name + '/' + 'data_val.npy'
        self.sh.cal.events_val_path = PATH_TO_SESSION + self.sh.info.name + '/' + 'events_val.npy'

        self.sh.cal.flag = True
        self.sh.saveToPkl()

    def update_settings(self):

        ids = self.ids

        ids.n_trials.value = self.sh.cal.n_trials
        ids.cue_offset.value = self.sh.cal.cue_offset
        ids.pause_offset.value = self.sh.cal.pause_offset
        ids.end_trial_offset.value = self.sh.cal.end_trial_offset