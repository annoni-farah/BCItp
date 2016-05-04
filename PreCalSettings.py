from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import json

class PreCalSettings(Screen):
# layout
    def __init__ (self,**kwargs):
        super (PreCalSettings, self).__init__(**kwargs)

        box1 = BoxLayout(padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=20)
        
        button_save = Button(text="Save", size_hint_x=1, size_hint_y=0.5)
        button_save.bind(on_press= self.save_config)

        button_back = Button(text="Back", size_hint_x=1, size_hint_y=0.5)
        button_back.bind(on_press= self.change_to_cal)

        box2 = BoxLayout(size_hint_x=1, size_hint_y=1,padding=10, spacing=10, orientation='vertical')


        self.total_time = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Total Time (s)', multiline=False)

        self.relax_time = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Time to set Max (s)', multiline=False)

        self.ch_energy_right = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='Right - Channels to use in Energy Computation :1 2 3 ...)', multiline=False)

        self.ch_energy_left = TextInput(size_hint=(1, 0.8), font_size= 20,
            hint_text='Left - Channels to use in Energy Computation :1 2 3 ...)', multiline=False)

        box2.add_widget(self.ch_energy_left)
        box2.add_widget(self.ch_energy_right)
        box2.add_widget(self.relax_time)
        box2.add_widget(self.total_time)

        box1.add_widget(self.label_msg)
        box1.add_widget(box2)
        box1.add_widget(button_save)
        box1.add_widget(button_back)

        self.add_widget(box1)

    def change_to_cal(self,*args):
        self.manager.current = 'PreCalMenu'
        self.manager.transition.direction = 'right'

    def save_config(self,*args):

        with open("data/rafael" + "/precal_config.txt", "w") as file:

            file.write(json.dumps({'ch_energy_left': self.ch_energy_left.text,
                 'ch_energy_right': self.ch_energy_right.text,
                 'total_time': self.total_time.text,
                 'relax_time': self.relax_time.text, }, file, indent=4))
                                
    

        self.label_msg.text = "Settings Saved!"
