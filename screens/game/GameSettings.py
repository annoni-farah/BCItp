############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty, \
                            ListProperty, BooleanProperty
from kivy.lang import Builder

# KV file:
Builder.load_file('screens/game/gamesettings.kv')

# Generic:

# Project's:
from SampleManager import *
from standards import *
from approach import Approach
######################################################################


class GameSettings(Screen):

    game_threshold = ObjectProperty(None)
    window_overlap = ObjectProperty(None)

    msg = StringProperty('')

# layout
    def __init__ (self, session_header,**kwargs):
        super (GameSettings, self).__init__(**kwargs)
        self.sh = session_header

    def change_to_game(self,*args):

        self.manager.current = 'GameMenu'
        self.manager.transition.direction = 'right'

    def enable_notch_filt(self, checkbox, value):
        
        print 'val:', value
        if value:
            self.notch = True
        else:
            self.notch = False


    def save_config(self,*args):

        self.sh.game_threshold = float(self.game_threshold.text)
        self.sh.window_overlap = float(self.window_overlap.text)

        self.sh.saveToPkl()
        self.msg = "Settings Saved!"
