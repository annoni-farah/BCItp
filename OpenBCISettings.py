from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import json

class OpenBCISettings(Screen):
# layout
    def __init__ (self,**kwargs):
        super (OpenBCISettings, self).__init__(**kwargs)

        box1 = BoxLayout(padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=20)
        
        button_save = Button(text="Save", size_hint_x=1, size_hint_y=0.5)
        button_save.bind(on_press= self.save_config)

        button_back = Button(text="Back", size_hint_x=1, size_hint_y=0.5)
        button_back.bind(on_press= self.change_to_cal)

        box2 = BoxLayout(size_hint_x=1, size_hint_y=1,padding=10, spacing=10, orientation='vertical')


        self.com_port = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='COM port', multiline=False)

        self.baud_rate = TextInput(size_hint=(1, 0.8), font_size= 20,
                        hint_text='Baud Rate', multiline=False)

        self.ch_labels = TextInput(size_hint=(1, 0.8), font_size= 20,
                hint_text='Channels Labels :Cz C4 C3 ...', multiline=False)

        box2.add_widget(self.com_port)
        box2.add_widget(self.baud_rate)
        box2.add_widget(self.ch_labels)

        box1.add_widget(self.label_msg)
        box1.add_widget(box2)
        box1.add_widget(button_save)
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

    def save_config(self,*args):
        
        self.load_session_config()

        with open("data/session/"+ self.session + "/openbci_config.txt", "w") as file:

            file.write(json.dumps({'com_port': self.com_port.text,
                                  'ch_labels': self.ch_labels.text,
                                  'baud_rate': self.baud_rate.text,
                                }, file, indent=4))
    

        self.label_msg.text = "Settings Saved!"
