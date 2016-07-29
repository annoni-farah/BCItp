############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# KV file:
Builder.load_file('screens/precal/precalmenu.kv')

# Generic:

# Project's:
from standards import *
######################################################################

class PreCalMenu(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (PreCalMenu, self).__init__(**kwargs)
        self.sh = session_header

    def change_to_acquisition(self,*args):
        self.manager.current = 'PreCalStart'
        self.manager.transition.direction = 'left'

    def change_to_calsettings(self,*args):
        self.manager.current = 'PreCalSettings'
        self.manager.transition.direction = 'left'

    def change_to_bci(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'