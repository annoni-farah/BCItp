from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

import json

from standards import *

class PreCalSettings(Screen):
# layout
    def __init__ (self,**kwargs):
        super (PreCalSettings, self).__init__(**kwargs)

        boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3, 
            padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=FONT_SIZE)
        
        button_save = Button(text="Save", size = BUTTON_SIZE)
        button_save.bind(on_press= self.save_config)

        button_default = Button(text="Load Default Config", size = BUTTON_SIZE)
        button_default.bind(on_press= self.load_default_settings)

        button_back = Button(text="Back", size = BUTTON_SIZE)
        button_back.bind(on_press= self.change_to_cal)

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.5,
            padding=10, spacing=10, orientation='vertical')


        self.total_time = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        hint_text='Total Time (s)', multiline=False)

        self.relax_time = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        hint_text='Time to set Max (s)', multiline=False)

        self.ch_energy_right = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                hint_text='Right - Channels to use in Energy Computation :1 2 3 ...)', multiline=False)

        self.ch_energy_left = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
            hint_text='Left - Channels to use in Energy Computation :1 2 3 ...)', multiline=False)

        self.sign_direction = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
            hint_text='Sign - left or right', multiline=False)

        checkbox_plot = CheckBox()
        checkbox_plot.bind(active=self.enable_plot)

        box_top.add_widget(self.sign_direction)
        box_top.add_widget(self.ch_energy_left)
        box_top.add_widget(self.ch_energy_right)
        box_top.add_widget(self.relax_time)
        box_top.add_widget(self.total_time)

        label_plot = Label(text="Plot Data:", font_size=FONT_SIZE)
        box_checkbox = BoxLayout(orientation='horizontal')

        box_checkbox.add_widget(label_plot)
        box_checkbox.add_widget(checkbox_plot)

        box_top.add_widget(box_checkbox)


        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_save)
        box_bottom.add_widget(button_default)
        box_bottom.add_widget(button_back)

        boxg.add_widget(box_top)
        boxg.add_widget(box_bottom)

        self.add_widget(boxg)

        # Default Values:
        self.plot_flag = False

    def change_to_cal(self,*args):
        self.manager.current = 'PreCalMenu'
        self.manager.transition.direction = 'right'

    def enable_plot(self, checkbox, value):
        if value:
            self.plot_flag = True
        else:
            self.plot_flag = False

    def load_session_config(self):
        PATH_TO_SESSION_LIST = 'data/session/session_list.txt'

        with open(PATH_TO_SESSION_LIST, "r") as data_file:    
            data = json.load(data_file)
            session_list = data["session_list"]
            self.session = session_list[-1]

    def load_default_settings(self,*args):
        PATH_TO_DEFAULT = 'data/default_configs/precal_config.txt'

        with open(PATH_TO_DEFAULT, "r") as data_file:    
            data = json.load(data_file)
            self.ch_energy_left.text = data["ch_energy_left"]
            self.ch_energy_right.text = data["ch_energy_right"]
            self.total_time.text = data["total_time"]
            self.relax_time.text = data["relax_time"]
            self.sign_direction.text = data["sign_direction"]

    def save_config(self,*args):
        self.load_session_config()

        with open("data/session/"+ self.session + "/precal_config.txt", "w") as file:

            file.write(json.dumps({'ch_energy_left': self.ch_energy_left.text,
                 'ch_energy_right': self.ch_energy_right.text,
                 'total_time': self.total_time.text,
                 'relax_time': self.relax_time.text, 
                 'sign_direction': self.sign_direction.text, 
                 'plot_flag': self.plot_flag, 
                 }, file, indent=4))
                                
    

        self.label_msg.text = "Settings Saved!"
