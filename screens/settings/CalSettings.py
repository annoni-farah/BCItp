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

        self.sh.n_trials = ids.n_trials.value
        self.sh.cue_offset = ids.cue_offset.value
        self.sh.pause_offset = ids.pause_offset.value
        self.sh.end_trial_offset = ids.end_trial_offset.value

        self.sh.saveToPkl()

    def update_settings(self):

        ids = self.ids

        if self.sh.n_trials != None:
            ids.n_trials.value = self.sh.n_trials
            ids.cue_offset.value = self.sh.cue_offset
            ids.pause_offset.value = self.sh.pause_offset
            ids.end_trial_offset.value = self.sh.end_trial_offset