from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import os

import json

from standards import *

BUTTON_SIZE = (100, 300)
TEXT_SIZE = (1, 0.7)

class StartScreen(Screen):
# layout
    def __init__ (self,**kwargs):
        super (StartScreen, self).__init__(**kwargs)

        boxg = AnchorLayout(anchor_x='center', anchor_y='center')

        box1 = BoxLayout(size_hint = (0.5, 0.5), padding=10, spacing=10,
                         orientation='vertical')

        self.label_msg = Label(text="", font_size=FONT_SIZE)

        button_ui_settings = Button(text="UIX Settings", font_size = FONT_SIZE ,
            width = 100, height= 50)
        button_ui_settings.bind(on_press= self.change_to_ui_settings)

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

    def change_to_ui_settings(self,*args):
        self.manager.current = 'UISettings'
        self.manager.transition.direction = 'left'

    def change_to_bci(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'left'

    def save_session_name(self,*args):

        PATH_TO_SESSION_LIST = 'data/session/session_list.txt'
        PATH_TO_SESSION = 'data/session/'

        if not os.path.isdir(PATH_TO_SESSION):
            os.makedirs(PATH_TO_SESSION)

        if os.path.isfile(PATH_TO_SESSION_LIST):
            pass
        else:
            # Creates session_list json file
            with open(PATH_TO_SESSION_LIST, "w") as file:
                file.write(json.dumps({'session_list': [''], }, file, indent=4))

        with open(PATH_TO_SESSION_LIST, "r") as data_file:    
            data = json.load(data_file)
            session_list = data["session_list"]

            print session_list

        if self.session_name.text in session_list:
           self.label_msg.text = "Session " + self.session_name.text + " already exists. Data will be overwritten"
           old_idx = session_list.index(self.session_name.text)
           session_list.append(session_list.pop(old_idx)) # move session name to the end of list

           print session_list

        else:
            self.label_msg.text = "Session Saved as: " + self.session_name.text
            os.makedirs(PATH_TO_SESSION + self.session_name.text)
            session_list.append(self.session_name.text)

            print session_list

        with open(PATH_TO_SESSION_LIST, "w") as file:

            print session_list

            file.write(json.dumps({'session_list': session_list, }, file, indent=4))