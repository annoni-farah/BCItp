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

        boxg = BoxLayout(padding=10, spacing=10, orientation='vertical')

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=20)
        
        button_save = Button(text="Save", size_hint_x=1, size_hint_y=0.5)
        button_save.bind(on_press= self.save_config)

        button_default = Button(text="Load Default Config", size_hint_x=1, size_hint_y=0.5)
        button_default.bind(on_press= self.load_default_settings)

        button_back = Button(text="Back", size_hint_x=1, size_hint_y=0.5)
        button_back.bind(on_press= self.change_to_cal)

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, spacing=10, orientation='vertical')

        self.n_trials = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Number of Trials', multiline=False)

        self.pause_offset = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Pause Offset', multiline=False)

        self.cue_offset = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Cue Offset', multiline=False)

        self.end_trial_offset = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='End of Trial Offset', multiline=False)


        box_top.add_widget(self.n_trials)
        box_top.add_widget(self.pause_offset)
        box_top.add_widget(self.cue_offset)
        box_top.add_widget(self.end_trial_offset)

        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_save)
        box_bottom.add_widget(button_default)
        box_bottom.add_widget(button_back)

        boxg.add_widget(box_top)
        boxg.add_widget(box_bottom)

        self.add_widget(boxg)


    def change_to_cal(self,*args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'right'

    def load_session_config(self):
        PATH_TO_SESSION_LIST = 'data/session/session_list.txt'

        with open(PATH_TO_SESSION_LIST, "r") as data_file:    
            data = json.load(data_file)
            session_list = data["session_list"]
            self.session = session_list[-1]

    def load_default_settings(self,*args):
        PATH_TO_DEFAULT = 'data/default_configs/cal_config.txt'

        with open(PATH_TO_DEFAULT, "r") as data_file:    
            data = json.load(data_file)
            self.n_trials.text = data["n_trials"]
            self.cue_offset.text = data["cue_offset"]
            self.pause_offset.text = data["pause_offset"]
            self.end_trial_offset.text = data["end_trial_offset"]


    def save_config(self,*args):
        self.load_session_config()

        with open("data/session/"+ self.session + "/cal_config.txt", "w") as file:

            file.write(json.dumps({'n_trials': self.n_trials.text, 
                'cue_offset': self.cue_offset.text, 
                'pause_offset': self.pause_offset.text, 
                'end_trial_offset': self.end_trial_offset.text}, file, indent=4))
    

        self.label_msg.text = "Settings Saved!"
