from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file('screens/bcimenu.kv')


class BCIMenu(Screen):
    # layout

    def __init__(self, session_header, **kwargs):
        super(BCIMenu, self).__init__(**kwargs)
        self.sh = session_header

    def change_to_calibration(self, *args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'left'

    def change_to_ml(self, *args):
        self.manager.current = 'MlMenu'
        self.manager.transition.direction = 'left'

    def change_to_game(self, *args):
        self.manager.current = 'GameMenu'
        self.manager.transition.direction = 'left'

    def change_to_openbci(self, *args):
        self.manager.current = 'AcquisitionSettings'
        self.manager.transition.direction = 'left'

    def change_to_start(self, *args):
        self.manager.current = 'start'
        self.manager.transition.direction = 'right'
