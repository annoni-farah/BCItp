from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import json

class DataProcessingSettings(Screen):
# layout
    def __init__ (self,**kwargs):
        super (DataProcessingSettings, self).__init__(**kwargs)

        box1 = BoxLayout(padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=20)
        
        button_save = Button(text="Save", size_hint_x=1, size_hint_y=0.5)
        button_save.bind(on_press= self.save_config)

        button_default = Button(text="Load Default Config", size_hint_x=1, size_hint_y=0.5)
        button_default.bind(on_press= self.load_default_settings)

        button_back = Button(text="Back", size_hint_x=1, size_hint_y=0.5)
        button_back.bind(on_press= self.change_to_cal)

        box2 = BoxLayout(size_hint_x=1, size_hint_y=1,padding=10, spacing=10, orientation='vertical')

        self.buf_len = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='Circular Buffer Length (in samples - min 125)', multiline=False)

        self.channels = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='Channels to use in Computation :1 2 3 ...', multiline=False)

        box3 = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='horizontal')

        self.f_high = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='Upper cutoff frequency (Hz)', multiline=False)

        self.f_low = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='Lower cutoff frequency (Hz)', multiline=False)

        self.f_order = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='Filter Order', multiline=False)

        box4 = BoxLayout(size_hint_x=1, size_hint_y=1,padding=10, spacing=10, orientation='horizontal')
        
        self.epoch_start = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Epoch Start', multiline=False)

        self.epoch_end = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Epoch End', multiline=False)

        box4.add_widget(self.epoch_start)
        box4.add_widget(self.epoch_end)

        box3.add_widget(self.f_low)
        box3.add_widget(self.f_high)
        box3.add_widget(self.f_order)

        box2.add_widget(self.channels)
        box2.add_widget(self.buf_len)

        box1.add_widget(self.label_msg)
        box1.add_widget(box4)
        box1.add_widget(box3)
        box1.add_widget(box2)
        box1.add_widget(button_save)
        box1.add_widget(button_default)
        box1.add_widget(button_back)

        self.add_widget(box1)

    def change_to_cal(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def load_session_config(self):
        PATH_TO_SESSION_LIST = 'data/session/session_list.txt'

        with open(PATH_TO_SESSION_LIST, "r") as data_file:    
            data = json.load(data_file)
            session_list = data["session_list"]
            self.session = session_list[-1]

    def load_default_settings(self,*args):
        PATH_TO_DEFAULT = 'data/default_configs/dp_config.txt'

        with open(PATH_TO_DEFAULT, "r") as data_file:    
            data = json.load(data_file)
            self.buf_len.text = data["buf_len"]
            self.channels.text = data["channels"]
            self.f_low.text = data["f_low"]
            self.f_high.text = data["f_high"]
            self.f_order.text = data["f_order"]
            self.epoch_start.text = data["epoch_start"]
            self.epoch_end.text = data["epoch_end"]

    def save_config(self,*args):

        self.load_session_config()

        if self.channels.text == "":
            self.channels.text = "1 2 3 4 5 6 7 8"

        with open("data/session/"+ self.session + "/dp_config.txt", "w") as file:

            file.write(json.dumps({'buf_len': self.buf_len.text, 
                'channels': self.channels.text, 
                'f_low': self.f_low.text, 
                'f_high': self.f_high.text,
                'f_order': self.f_order.text,
                'epoch_start': self.epoch_start.text,
                'epoch_end': self.epoch_end.text,
                }, file, indent=4))
    

        self.label_msg.text = "Settings Saved!"
