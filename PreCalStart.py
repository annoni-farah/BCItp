from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from SampleManager import *

import thread

class PreCalStart(Screen):
# layout
    def __init__ (self,**kwargs):
        super (PreCalStart, self).__init__(**kwargs)

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='vertical')


        button_back = Button(text="Back")
        button_back.bind(on_press= self.change_to_precal)

        button_stream = Button(text="Start Streaming")
        button_stream.bind(on_press= self.openbci_stream)

        box1.add_widget(button_stream)
        box1.add_widget(button_back)

        self.add_widget(box1) 

    def change_to_precal(self,*args):
        self.manager.current = 'PreCalMenu'
        self.manager.transition.direction = 'right'

    def openbci_stream(self,*args):
        sm = SampleManager()

        sm.hw_stream()
        