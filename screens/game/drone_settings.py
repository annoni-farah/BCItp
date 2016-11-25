# DEPENDENCIES --------------------------
# Project's:

# KIVY modules:
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# KV file:
Builder.load_file('bcitp/screens/game/drone_settings.kv')

# Generic:
######################################################################


class DroneSettings(Screen):

    # layout
    def __init__(self, session_header, **kwargs):
        super(DroneSettings, self).__init__(**kwargs)
        self.sh = session_header

    def change_to_drone(self, *args):

        self.manager.current = 'DroneMenu'
        self.manager.transition.direction = 'right'

    def save_config(self, *args):

        ids = self.ids

        self.sh.game.game_threshold = ids.game_threshold.value
        self.sh.game.window_overlap = ids.window_overlap.value / 1000.0
        self.sh.game.warning_threshold = ids.warning_threshold.value
        self.sh.game.forward_speed = ids.forward_speed.value / 1000.0
        self.sh.game.inst_prob = ids.inst_prob.value / 1000.0
        self.sh.game.keyb_enable = ids.keyb_enable.value

        self.sh.game.action_cmd1 = ids.action_cmd1.value
        self.sh.game.action_cmd2 = ids.action_cmd2.value

        self.sh.game.flag = True
        self.sh.saveToPkl()

    def update_settings(self):

        ids = self.ids
