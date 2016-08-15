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
from standards import *
######################################################################


class GameSettings(Screen):

    game_threshold = ObjectProperty(None)
    window_overlap = ObjectProperty(None)
    warning_threshold = ObjectProperty(None)
    forward_speed = ObjectProperty(None)

    msg = StringProperty('')

# layout
    def __init__ (self, session_header,**kwargs):
        super (GameSettings, self).__init__(**kwargs)
        self.sh = session_header

    def change_to_game(self,*args):

        self.manager.current = 'GameMenu'
        self.manager.transition.direction = 'right'

    def save_config(self,*args):

        ids = self.ids

        self.sh.game_threshold = ids.game_threshold.value
        self.sh.window_overlap = ids.window_overlap.value / 1000.0
        self.sh.warning_threshold = ids.warning_threshold.value 
        self.sh.forward_speed = ids.forward_speed.value / 1000.0
        self.sh.inst_prob = ids.inst_prob.value / 1000.0

        self.sh.saveToPkl()
