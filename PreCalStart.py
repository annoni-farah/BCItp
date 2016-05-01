from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.clock import Clock

# from threading import Thread
from SampleManager import *

class PreCalStart(Screen):
# layout
    def __init__ (self,**kwargs):
        super (PreCalStart, self).__init__(**kwargs)

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='vertical')


        button_back = Button(text="Back")
        button_back.bind(on_press= self.change_to_precal)

        self.button_stream = Button(text="Start Streaming")
        self.button_stream.bind(on_press= self.bci_begin)

        self.label_energy = Label()


        box1.add_widget(self.label_energy)
        box1.add_widget(self.button_stream)
        box1.add_widget(button_back)

        self.add_widget(box1) 

        self.stream_flag = False

        Clock.schedule_interval(self.get_energy, 1)

    def change_to_precal(self,*args):
        self.manager.current = 'PreCalMenu'
        self.manager.transition.direction = 'right'

    def bci_begin(self,*args):

        if self.stream_flag:
            self.button_stream.text = 'Start Streaming'
            self.sm.stop_flag = True
            self.stream_flag = False
            self.label_energy.text = ""
            self.sm.join()

        else:
            self.sm = SampleManager()
            self.sm.daemon = True
            self.button_stream.text = 'Stop Streaming'
            self.sm.stop_flag = False
            self.sm.start()
            self.stream_flag = True

    def get_energy(self, dt):
        if self.stream_flag:
            energy = self.sm.ComputeEnergy()
            self.label_energy.text = "Energy level : {} and {}".format(energy, self.sm.counter)



        