from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.clock import Clock

# from threading import Thread
from SampleManager import *

from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

from kivy.graphics import Rectangle, Color

import json

class CalStart(Screen):
# layout
    def __init__ (self,**kwargs):
        super (CalStart, self).__init__(**kwargs)

        box = BoxLayout(size_hint_x=1, size_hint_y=1,padding=10, spacing=10, orientation='vertical')

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='vertical')
        box2 = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='vertical')

        button_back = Button(text="Back")
        button_back.bind(on_press= self.change_to_precal)

        self.button_stream = Button(text="Start Streaming")
        self.button_stream.bind(on_press= self.bci_begin)

        # self.button_save = Button(text="Save Data")
        # self.button_save.bind(on_press= self.save_data)

        self.carousel = Carousel(direction='right')
        for i in range(10):
            src = "http://placehold.it/480x270.png&text=slide-%d&.png" % i
            image = AsyncImage(source=src, allow_stretch=True)
            self.carousel.add_widget(image)

        self.label_energy = Label()


        box2.add_widget(self.carousel)

        box1.add_widget(self.label_energy)

        # box1.add_widget(self.button_save)
        box1.add_widget(self.button_stream)
        box1.add_widget(button_back)

        box.add_widget(box2) 
        box.add_widget(box1) 

        self.add_widget(box)

        self.stream_flag = False

        self.load_dp_settings()
        self.load_openbci_settings()

    def change_to_precal(self,*args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'right'

    def bci_begin(self,*args):

        if self.stream_flag:
            self.button_stream.text = 'Start Streaming'
            self.sm.stop_flag = True
            self.stream_flag = False
            self.sm.join()
            self.clock_unscheduler()

        else:
            self.sm = SampleManager(self.com_port, self.baud_rate, rec = True)

            self.sm.CreateDataProcessing(self.channels, self.buf_len, 
                                        self.f_low, self.f_high, self.f_order)

            self.sm.daemon = True  
            self.sm.stop_flag = False
            self.sm.start()
            self.stream_flag = True
            self.button_stream.text = 'Stop Streaming'
            self.clock_scheduler()

    def get_energy(self, dt):
        if self.stream_flag:
            energy = self.sm.ComputeEnergy()
            if not energy == None:
                self.label_energy.text = "Energy level : {}".format(energy)

    def clock_scheduler(self):
        # Clock.schedule_interval(self.get_energy, 1/6)
        Clock.schedule_interval(self.save_data, 10)
        Clock.schedule_once(self.schedule_first_sign, 1)
        Clock.schedule_once(self.schedule_second_sign, 3)
        Clock.schedule_once(self.schedule_third_sign, 5)

    def clock_unscheduler(self):
        Clock.unschedule(self.set_sign_pause)
        Clock.unschedule(self.set_sign_left)
        Clock.unschedule(self.set_sign_right)
        Clock.unschedule(self.get_energy)
        Clock.unschedule(self.save_data)

    def schedule_first_sign(self, dt):
        Clock.schedule_interval(self.set_sign_pause, 1)

    def schedule_second_sign(self, dt):
        Clock.schedule_interval(self.set_sign_left, 1)

    def schedule_third_sign(self, dt):
        Clock.schedule_interval(self.set_sign_right, 1)

    def set_sign_pause(self, dt):
        self.carousel.index = 0
        self.sm.MarkEvents(0)

    def set_sign_left(self, dt):
        self.carousel.index = 1
        self.sm.MarkEvents(1)

    def set_sign_right(self, dt):
        self.carousel.index = 2
        self.sm.MarkEvents(2)

    def load_dp_settings(self):

        # if os.path.exists("data/rafael/precal_config"):
        with open("data/rafael" + "/dp_config.txt", "r") as data_file:    
            data = json.load(data_file)

        self.buf_len = int(data["buf_len"])
        self.f_low = int(data["f_low"])
        self.f_high = int(data["f_high"])
        self.f_order = int(data["f_order"])
        self.channels = map(int, data['channels'].split(" "))

    def load_openbci_settings(self):

        # if os.path.exists("data/rafael/precal_config"):
        with open("data/rafael" + "/openbci_config.txt", "r") as data_file:    
            data = json.load(data_file)

        self.com_port = data["com_port"]
        self.ch_labels = data["ch_labels"]
        self.baud_rate = data["baud_rate"]

    def load_cal_settings(self):

        # if os.path.exists("data/rafael/precal_config"):
        with open("data/rafael" + "/cal_config.txt", "r") as data_file:    
            data = json.load(data_file)

        self.n_trials = data["n_trials"]
        self.cue_offset = data["cue_offset"]
        self.pause_offset = data["pause_offset"]
        self.epoch_start = data["epoch_start"]
        self.epoch_end = data["epoch_end"]

    def save_data(self, dt):
        print "Saving data"
        self.sm.SaveData()
        self.sm.SaveEvents()