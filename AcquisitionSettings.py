from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

import json

class AcquisitionSettings(Screen):
# layout
    def __init__ (self,**kwargs):
        super (AcquisitionSettings, self).__init__(**kwargs)

        boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.6,
            padding=10, spacing=10, orientation='vertical')

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.4, 
            padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=20)
        
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


        self.box_text = BoxLayout(size_hint_x=1, size_hint_y=0.7,
            padding=10, spacing=10, )

        self.box_text_openbci = BoxLayout(orientation='vertical')

        self.com_port = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='COM port', multiline=False)

        self.baud_rate = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Baud Rate', multiline=False)

        self.ch_labels = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='Channels Labels :Cz C4 C3 ...', multiline=False)

        self.box_text_openbci.add_widget(self.com_port)
        self.box_text_openbci.add_widget(self.baud_rate)
        self.box_text_openbci.add_widget(self.ch_labels)

        self.box_text_simu = BoxLayout(orientation='vertical')

        self.ch_labels = TextInput(font_size= 20,
                hint_text='Channels Labels :Cz C4 C3 ...', multiline=False)

        self.ch_labels.width = 200
        self.ch_labels.height = (self.ch_labels.minimum_height)
        print 'min height:', self.ch_labels.minimum_height

        self.box_text_simu.add_widget(self.ch_labels)

        self.box_text_playback = BoxLayout(orientation='vertical')

        self.path_to_file = TextInput(font_size= 20,
                hint_text='Path to EEG file', multiline=False)

        self.box_text_playback.add_widget(self.path_to_file)

        label_simu = Label(text="Simulator", font_size=20)
        label_openbci = Label(text="OpenBCI", font_size=20)
        label_playback = Label(text="Playback", font_size=20)

        box_checkbox = BoxLayout(size_hint_x=1, size_hint_y=0.3,
                        padding=5, spacing=5, orientation='vertical')

        box_checkbox_top = BoxLayout(size_hint_x=1, size_hint_y=0.5,
                        padding=5, spacing=5, orientation='horizontal')

        box_checkbox_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.5,
                        padding=5, spacing=5, orientation='horizontal')


        checkbox_simu = CheckBox()
        checkbox_simu.bind(active=self.enable_simu_config)

        checkbox_openbci = CheckBox()
        checkbox_openbci.bind(active=self.enable_openbci_config)

        checkbox_playback = CheckBox()
        checkbox_playback.bind(active=self.enable_playback_config)
        
        box_checkbox_bottom.add_widget(checkbox_simu)
        box_checkbox_bottom.add_widget(checkbox_openbci)
        box_checkbox_bottom.add_widget(checkbox_playback)

        box_checkbox_top.add_widget(label_simu)
        box_checkbox_top.add_widget(label_openbci)
        box_checkbox_top.add_widget(label_playback)

        box_checkbox.add_widget(box_checkbox_top)
        box_checkbox.add_widget(box_checkbox_bottom)

        box_top.add_widget(box_checkbox)
        box_top.add_widget(self.box_text)

        boxg.add_widget(box_top)
        boxg.add_widget(box_bottom)

        self.add_widget(boxg)

    def change_to_cal(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def enable_openbci_config(self, checkbox, value):
        if value:
            self.box_text.add_widget(self.box_text_openbci)
            self.mode = 'openbci'
        else:
            self.box_text.remove_widget(self.box_text_openbci)

    def enable_simu_config(self, checkbox, value):
        if value:
            self.box_text.add_widget(self.box_text_simu)
            self.mode = 'simu'
        else:
            self.box_text.remove_widget(self.box_text_simu)

    def enable_playback_config(self, checkbox, value):
        if value:
            self.box_text.add_widget(self.box_text_playback)
            self.mode = 'playback'
        else:
            self.box_text.remove_widget(self.box_text_playback)

    def load_session_config(self):
        PATH_TO_SESSION_LIST = 'data/session/session_list.txt'

        with open(PATH_TO_SESSION_LIST, "r") as data_file:    
            data = json.load(data_file)
            session_list = data["session_list"]
            self.session = session_list[-1]

    def load_default_settings(self,*args):
        PATH_TO_DEFAULT = 'data/default_configs/openbci_config.txt'

        with open(PATH_TO_DEFAULT, "r") as data_file:    

            data = json.load(data_file)
            if self.mode == 'openbci':
                self.com_port.text = data["com_port"]
                self.baud_rate.text = data["baud_rate"]
                self.ch_labels.text = data["ch_labels"]

            elif self.mode == 'simu':
                self.ch_labels.text = data["ch_labels"]

            elif self.mode == 'playback':
                self.path_to_file.text = data["path_to_file"]

    def save_config(self,*args):
        
        self.load_session_config()

        with open("data/session/"+ self.session + "/openbci_config.txt", "w") as file:
            if self.mode == 'openbci':
                file.write(json.dumps({'com_port': self.com_port.text,
                                      'ch_labels': self.ch_labels.text,
                                      'baud_rate': self.baud_rate.text,
                                      'mode': self.mode,
                                    }, file, indent=4))

            elif self.mode == 'simu':
                file.write(json.dumps({'ch_labels': self.ch_labels.text,
                                      'mode': self.mode,
                                    }, file, indent=4))

            elif self.mode == 'playback':
                file.write(json.dumps({'path_to_file': self.path_to_file.text,
                                      'mode': self.mode,
                                    }, file, indent=4))
    

        self.label_msg.text = "Settings Saved!"

