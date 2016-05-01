from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import json

class CalSettings(Screen):
# layout
    def __init__ (self,**kwargs):
        super (CalSettings, self).__init__(**kwargs)

        box1 = BoxLayout(padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=20)
        
        button_save = Button(text="Save", size_hint_x=1, size_hint_y=0.5)
        button_save.bind(on_press= self.save_config)

        button_back = Button(text="Back", size_hint_x=1, size_hint_y=0.5)
        button_back.bind(on_press= self.change_to_cal)

        box2 = BoxLayout(size_hint_x=1, size_hint_y=1,padding=10, spacing=10, orientation='vertical')

        self.n_trials = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Number of Trials', multiline=False)

        self.cue_offset = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Cue Offset', multiline=False)

        self.pause_offset = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Pause Offset', multiline=False)

        box3 = BoxLayout(size_hint_x=1, size_hint_y=1,padding=10, spacing=10, orientation='horizontal')
        
        self.epoch_start = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Epoch Start', multiline=False)

        self.epoch_end = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Epoch End', multiline=False)

        box3.add_widget(self.epoch_start)
        box3.add_widget(self.epoch_end)

        box2.add_widget(self.n_trials)
        box2.add_widget(self.cue_offset)
        box2.add_widget(self.pause_offset)

        box1.add_widget(self.label_msg)
        box1.add_widget(box3)
        box1.add_widget(box2)
        box1.add_widget(button_save)
        box1.add_widget(button_back)

        self.add_widget(box1)

    def change_to_cal(self,*args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'right'

    def save_config(self,*args):

        with open("data/rafael" + "/cal_config.txt", "w") as file:

            file.write(json.dumps({'n_trials': self.n_trials.text, 'cue_offset': self.cue_offset.text, 
                'pause_offset': self.pause_offset.text, 'epoch_start': self.epoch_start.text,
                'epoch_end': self.epoch_end.text}, file, indent=4))
    

        self.label_msg.text = "Settings Saved!"
