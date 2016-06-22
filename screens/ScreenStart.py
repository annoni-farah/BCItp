from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import os

import json

from standards import *
from kivy_utils import ErrorPopup

TEXT_SIZE = (1, 0.7)

class StartScreen(Screen):
# layout
    def __init__ (self, session_header, **kwargs):
        super (StartScreen, self).__init__(**kwargs)

        self.sh = session_header

        boxg = AnchorLayout(anchor_x='center', anchor_y='center')

        box1 = BoxLayout(size_hint = (0.5, 0.5), padding=10, spacing=10,
                         orientation='vertical')

        self.label_msg = Label(text="", font_size=FONT_SIZE)

        button_ui_settings = Button(text="General Settings", font_size = FONT_SIZE,
            size = BUTTON_SIZE)
        button_ui_settings.bind(on_press= self.change_to_gen_settings)

        button_next = Button(text="BCI Menu", size=BUTTON_SIZE, font_size = FONT_SIZE)
        button_next.bind(on_press= self.change_to_bci)

        button_save = Button(text="Save", size=BUTTON_SIZE, font_size = FONT_SIZE)
        button_save.bind(on_press= self.save_session_name)

        self.session_name = TextInput(font_size= FONT_SIZE, size_hint=TEXT_SIZE,
            hint_text='Session Name', multiline=False)

        box1.add_widget(self.label_msg)
        box1.add_widget(self.session_name)
        box1.add_widget(button_save)
        box1.add_widget(button_ui_settings)
        box1.add_widget(button_next)

        # box1.size = box1.minimum_size

        boxg.add_widget(box1)

        self.add_widget(boxg)

    def change_to_gen_settings(self,*args):
        self.manager.current = 'GeneralSettings'
        self.manager.transition.direction = 'left'

    def change_to_bci(self,*args):

        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'left'

    def save_session_name(self,*args):

        sname = self.session_name.text
        self.sh.name = sname


        if not os.path.isdir(PATH_TO_SESSION):
            os.makedirs(PATH_TO_SESSION)

        if os.path.isdir(PATH_TO_SESSION + sname):

            self.label_msg.text = "Session " + sname + " already exists. Data will be overwritten"
            self.sh.loadFromPkl()

        else:
            os.makedirs(PATH_TO_SESSION + sname)
            self.sh.saveToPkl()
            self.label_msg.text = "Session Saved as: " + sname

        self.sh.data_cal_path = PATH_TO_SESSION + self.sh.name + '/' + 'data_cal.txt'
        self.sh.events_cal_path = PATH_TO_SESSION + self.sh.name + '/' + 'events_cal.txt'
        self.sh.data_val_path = PATH_TO_SESSION + self.sh.name + '/' + 'data_val.txt'
        self.sh.events_val_path = PATH_TO_SESSION + self.sh.name + '/' + 'events_val.txt'