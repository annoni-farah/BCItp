from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.image import AsyncImage

from kivy.graphics import Rectangle, Color

from kivy.clock import Clock

# from threading import Thread
from SampleManager import *

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty

from time import sleep

import json


class PreCalStart(Screen):
# layout
    def __init__ (self,**kwargs):
        super (PreCalStart, self).__init__(**kwargs)

        box_vleft = BoxLayout(size_hint_x=0.1, size_hint_y=0.7,padding=10, spacing=10, orientation='horizontal')
        box_vmiddle = BoxLayout(size_hint_x=0.8, size_hint_y=0.7,padding=10, spacing=10, orientation='horizontal')
        box_vright = BoxLayout(size_hint_x=0.1, size_hint_y=0.7,padding=10, spacing=10, orientation='horizontal')

        box_middle = FloatLayout()

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, spacing=10, orientation='vertical')

        button_back = Button(text="Back")
        button_back.bind(on_press= self.change_to_precal)

        self.button_stream = Button(text="Start Streaming")
        self.button_stream.bind(on_press= self.bci_begin)

        # self.label_info = Label(pos_hint={'center_x': .5, 'center_y': .5})

        button_change = Button(text="Invert")
        button_change.bind(on_press= self.change_arrow)

        src = "data/resources/left_arrow.png"

        image = AsyncImage(source=src, allow_stretch=False, pos_hint={'x': 1, 'y': 1})

        box_vmiddle.add_widget(image)

        # self.add_arrow(0)

        box_vmiddle.add_widget(box_middle)

        # self.box_middle.add_widget(self.label_info)

        # box1.add_widget(self.label_info)
        box1.add_widget(button_change)
        box1.add_widget(self.button_stream)
        box1.add_widget(button_back)

        self.add_widget(box_vleft)
        self.add_widget(box_vmiddle)
        self.add_widget(box_vright)
        self.add_widget(box1) 

       

        self.stream_flag = False

        self.load_settings()

    def change_to_precal(self,*args):

        self.manager.current = 'PreCalMenu'
        self.manager.transition.direction = 'right'

    def bci_begin(self,*args):

        if self.stream_flag:
            self.button_stream.text = 'Start Streaming'
            self.sm.stop_flag = True
            self.stream_flag = False
            self.label_info.text = ""
            self.sm.join()
            Clock.unschedule(self.get_energy)

        else:
            self.label_info.text = "Managing Samples..."
            self.sm = SampleManager()
            self.label_info.text = "Computing filters and creating buffers..."

            self.sm.CreateDataProcessing(self.channels, self.buf_len, self.f_low, self.f_high, self.f_order)

            Clock.schedule_interval(self.get_energy, 1/5)

            self.sm.daemon = True  
            self.sm.stop_flag = False
            self.label_info.text = "Now Streaming..."
            self.sm.start()
            self.stream_flag = True
            self.button_stream.text = 'Stop Streaming'

    def get_energy(self, dt):

        energy = self.sm.ComputeEnergy()
        self.label_info.text = "Energy level : {}".format(energy)

    def load_settings(self):

        with open("data/rafael" + "/precal_config.txt", "r") as data_file:    
            data = json.load(data_file)

        self.total_time = int(data["total_time"])
        self.buf_len = int(data["buf_len"])
        self.f_low = int(data["f_low"])
        self.f_high = int(data["f_high"])
        self.f_order = int(data["f_order"])

        self.channels = map(int, data['channels'].split(" "))

    def add_arrow(self, idx):

        if idx == 0:
            src = "data/resources/left_arrow.png"
        elif idx ==1:
            src = "data/resources/right_arrow.png"

        self.image = AsyncImage(source=src, allow_stretch=False, pos_hint={'center_x': 1, 'center_y': 1})

        self.box_middle.add_widget(self.image)

    def remove_arrow(self):

        self.box_middle.remove_widget(self.image)


    def change_arrow(self,*args):

        self.remove_arrow()
        self.add_arrow(1)

    


        