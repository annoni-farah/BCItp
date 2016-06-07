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

        boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label_msg = Label(text="", font_size=20)
        ## BOTTOM PART (BUTTONS)

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='vertical')

        button_save = Button(text="Save", size_hint_x=1, size_hint_y=0.5)
        button_save.bind(on_press= self.save_config)

        button_default = Button(text="Load Default Config", size_hint_x=1, size_hint_y=0.5)
        button_default.bind(on_press= self.load_default_settings)

        button_back = Button(text="Back", size_hint_x=1, size_hint_y=0.5)
        button_back.bind(on_press= self.change_to_cal)

        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_save)
        box_bottom.add_widget(button_default)
        box_bottom.add_widget(button_back)

        ## TOP PART

        # EPOCHS CONFIG
        box_epochs = BoxLayout(size_hint_x=1, size_hint_y=0.15,padding=10, spacing=10, orientation='horizontal')
        label_start = Label(text = 'Epoch Start')
        self.epoch_start = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='2', multiline=False)
        label_end = Label(text = 'Epoch End')
        self.epoch_end = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='4', multiline=False)

        box_epochs.add_widget(label_start)
        box_epochs.add_widget(self.epoch_start)
        box_epochs.add_widget(label_end)
        box_epochs.add_widget(self.epoch_end)
        
        boxg.add_widget(box_epochs)

        # DATA CONFIG
        box_data = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, spacing=10, orientation='vertical')

        box_buf = BoxLayout(orientation = 'horizontal')
        label_buf = Label(text ='Circular Buffer Length')
        self.buf_len = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='in samples - default 500', multiline=False)
        box_buf.add_widget(label_buf)
        box_buf.add_widget(self.buf_len)

        box_ch = BoxLayout(orientation = 'horizontal')
        label_ch = Label(text = 'Channels idx used')
        self.channels = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text=' 0 1 2 3 4 5 6 7 8', multiline=False)
        box_ch.add_widget(label_ch)
        box_ch.add_widget(self.channels)

        box_data.add_widget(box_buf)
        box_data.add_widget(box_ch)

        boxg.add_widget(box_data)


        # FILTER CONFIG
        box_filter = BoxLayout(size_hint_x=1, size_hint_y=0.15,padding=10, spacing=10, orientation='horizontal')

        box_high = BoxLayout(orientation = 'horizontal')
        label_high = Label(text = 'Upper cutoff freq')
        self.f_high = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='30 (Hz)', multiline=False)
        box_high.add_widget(label_high)
        box_high.add_widget(self.f_high)

        box_low = BoxLayout(orientation = 'horizontal')
        label_low = Label(text = 'Lower cutoff freq')
        self.f_low = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='8 (Hz)', multiline=False)
        box_low.add_widget(label_low)
        box_low.add_widget(self.f_low)


        box_order = BoxLayout(orientation = 'horizontal')
        label_order = Label(text = 'Filter Order')
        self.f_order = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='7', multiline=False)
        box_order.add_widget(label_order)
        box_order.add_widget(self.f_order)

        box_filter.add_widget(box_low)
        box_filter.add_widget(box_high)
        box_filter.add_widget(box_order)

        boxg.add_widget(box_filter)

        boxg.add_widget(box_bottom)

        self.add_widget(boxg)

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
