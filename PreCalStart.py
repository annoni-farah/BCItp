from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.image import AsyncImage

from kivy.uix.slider import Slider

from kivy.graphics import Rectangle, Color

from kivy.clock import Clock

# from threading import Thread
from SampleManager import *

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty

from time import sleep

import json

import os

from math import ceil


class PreCalStart(Screen):
# layout
    def __init__ (self,**kwargs):
        super (PreCalStart, self).__init__(**kwargs)


    # Top part
        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.7,padding=10, 
            spacing=10, orientation='horizontal')

        box_vleft = BoxLayout(size_hint_x=0.2)
        self.box_vmiddle = BoxLayout(size_hint_x=0.6, orientation='vertical')
        box_vright = BoxLayout(size_hint_x=0.2)

        self.s_left = Slider(min=0, max=100, orientation='vertical')
        self.s_right = Slider(min=0, max=100, orientation='vertical')
        self.label_info = Label(text= 'Msg:')

        box_vleft.add_widget(self.s_left, 0)
        box_vright.add_widget(self.s_right, 1)
        self.box_vmiddle.add_widget(self.label_info)


        box_top.add_widget(box_vleft, 0)
        box_top.add_widget(self.box_vmiddle, 1)
        box_top.add_widget(box_vright, 2)


    # Bottom part

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, 
            spacing=10, orientation='vertical')

        button_back = Button(text="Back")
        button_back.bind(on_press= self.change_to_precal)

        self.button_stream = Button(text="Start Streaming")
        self.button_stream.bind(on_press= self.bci_begin)

        button_bar_default = Button(text="Reset Bar Max")
        button_bar_default.bind(on_press= self.set_bar_default)

        box_bottom.add_widget(self.button_stream)
        box_bottom.add_widget(button_bar_default)
        box_bottom.add_widget(button_back)

    # Whole part

        boxg = BoxLayout(orientation='vertical', padding=10, 
            spacing=10)

        boxg.add_widget(box_bottom, 0)
        boxg.add_widget(box_top, 1)
        

        self.add_widget(boxg) 

        self.stream_flag = False

    def change_to_precal(self,*args):

        self.manager.current = 'PreCalMenu'
        self.manager.transition.direction = 'right'

    def set_bar_default(self,*args):
        self.s_right.max = 100
        self.s_left.max = 100

    def bci_begin(self,*args):

        if self.stream_flag:
            self.button_stream.text = 'Start Streaming'
            self.sm.stop_flag = True
            self.stream_flag = False
            self.label_info.text = ""
            self.sm.join()
            self.clock_unscheduler()
            self.remove_arrow()

        else:
            self.load_session_config()
            self.load_dp_settings()
            self.load_openbci_settings()
            self.load_precal_settings()

            self.add_arrow()
            
            self.label_info.text = "Managing Samples..."
            self.sm = SampleManager(self.com_port, self.baud_rate)
            self.label_info.text = "Computing filters and creating buffers..."

            self.sm.CreateDataProcessing(self.channels, self.buf_len, 
                self.f_low, self.f_high, self.f_order)
            self.sm.daemon = True  
            self.sm.stop_flag = False
            self.label_info.text = "Now Streaming..."
            self.sm.start()
            self.stream_flag = True
            self.button_stream.text = 'Stop Streaming'
            self.clock_scheduler()

    def clock_scheduler(self):
        Clock.schedule_interval(self.get_energy_left, 1/2)
        Clock.schedule_interval(self.get_energy_right, 1/2)
        Clock.schedule_once(self.bci_begin, self.total_time)
        Clock.schedule_once(self.set_bar_max, self.relax_time)

    def clock_unscheduler(self):
        Clock.unschedule(self.get_energy_left)
        Clock.unschedule(self.get_energy_right)
        Clock.unschedule(self.bci_begin)
        Clock.unschedule(self.set_bar_max)


    def get_energy_right(self, dt):

        energy = self.sm.ComputeEnergy(self.ch_energy_right)
        # self.label_info.text = "Energy level : {}".format(energy)
        if hasattr(self, 'bar_max'):
            self.s_right.value = ceil((energy / self.bar_max )*100)

    def get_energy_left(self, dt):

        energy = self.sm.ComputeEnergy(self.ch_energy_left)
        # self.label_info.text = "Energy level : {}".format(energy)
        if hasattr(self, 'bar_max'):
            self.s_left.value = ceil((energy / self.bar_max )*100)

    def load_session_config(self):
        PATH_TO_SESSION_LIST = 'data/session/session_list.txt'

        with open(PATH_TO_SESSION_LIST, "r") as data_file:    
            data = json.load(data_file)
            session_list = data["session_list"]
            self.session = session_list[-1]

    def load_dp_settings(self):

        # if os.path.exists("data/rafael/precal_config"):
        with open("data/session/"+ self.session + "/dp_config.txt", "r") as data_file:    
            data = json.load(data_file)

        self.buf_len = int(data["buf_len"])
        self.f_low = int(data["f_low"])
        self.f_high = int(data["f_high"])
        self.f_order = int(data["f_order"])
        self.channels = map(int, data['channels'].split())

    def load_openbci_settings(self):

        # if os.path.exists("data/rafael/precal_config"):
        with open("data/session/"+ self.session + "/openbci_config.txt", "r") as data_file:    
            data = json.load(data_file)

        self.com_port = data["com_port"]
        self.ch_labels = data["ch_labels"]
        self.baud_rate = int(data["baud_rate"])

    def load_precal_settings(self):

        # if os.path.exists("data/rafael/precal_config"):
        with open("data/session/"+ self.session + "/precal_config.txt", "r") as data_file:    
            data = json.load(data_file)

        self.ch_energy_right = map(int, data['ch_energy_right'].split(" "))
        self.ch_energy_left = map(int, data['ch_energy_left'].split(" "))
        self.total_time = int(data['total_time'])
        self.relax_time = int(data['relax_time'])
        self.sign_direction = data['sign_direction']

    def calc_bar_max(self):
        max_right = self.sm.CalcEnergyAverage(self.ch_energy_right)
        max_left = self.sm.CalcEnergyAverage(self.ch_energy_left)

        self.bar_max = max(max_right, max_left)

    def set_bar_max(self, dt):

        self.calc_bar_max()

        self.s_left.max = self.bar_max
        self.s_right.max = self.bar_max

    def calc_bar_th(self):

        self.bar_th = 0.3 * self.bar_max

    def set_bar_th(self, dt):

        self.calc_bar_th()

    def add_arrow(self):

        if self.sign_direction == 'left':
            src = "data/resources/left.png"
        elif self.sign_direction == 'right':
            src = "data/resources/right.png"

        self.image = AsyncImage(source=src, allow_stretch=False)

        self.box_vmiddle.add_widget(self.image)

    def remove_arrow(self):

        self.box_vmiddle.remove_widget(self.image)


    


        