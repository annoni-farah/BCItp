from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

from kivy.graphics import Rectangle, Color

import os

import json

from standards import *
from kivy_utils import ErrorPopup

from kivy.properties import ObjectProperty, StringProperty

Builder.load_file('screens/screenstart.kv')

class StartScreen(Screen):
# layout
    session_name = ObjectProperty(None)
    label_msg = StringProperty('')

    def __init__ (self, session_header, **kwargs):
        super (StartScreen, self).__init__(**kwargs)

        self.sh = session_header

    def change_to_gen_settings(self,*args):
        self.manager.current = 'GeneralSettings'
        self.manager.transition.direction = 'left'

    def change_to_bci(self,*args):

        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'left'

    def save_session_name(self,*args):

        sname = self.session_name.text

        if not os.path.isdir(PATH_TO_SESSION):
            os.makedirs(PATH_TO_SESSION)

        if sname == '':
            # if no session_name is provided, use latest modified folder in data/session
            all_subdirs = []
            for d in os.listdir(PATH_TO_SESSION + '.'):
                bd = os.path.join(PATH_TO_SESSION, d)
                if os.path.isdir(bd): all_subdirs.append(bd)
            sname = max(all_subdirs, key=os.path.getmtime).split('/')[2]

        self.sh.name = sname

        if os.path.isdir(PATH_TO_SESSION + sname):

            self.label_msg = "Session " + sname + " already exists. Data will be overwritten"
            self.sh.loadFromPkl()

        else:
            os.makedirs(PATH_TO_SESSION + sname)
            self.sh.saveToPkl()
            self.label_msg = "Session Saved as: " + sname

        self.sh.data_cal_path = PATH_TO_SESSION + self.sh.name + '/' + 'data_cal.npy'
        self.sh.events_cal_path = PATH_TO_SESSION + self.sh.name + '/' + 'events_cal.npy'
        self.sh.data_val_path = PATH_TO_SESSION + self.sh.name + '/' + 'data_val.npy'
        self.sh.events_val_path = PATH_TO_SESSION + self.sh.name + '/' + 'events_val.npy'