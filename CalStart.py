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

import random

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
        self.button_stream.bind(on_press= self.start)

        # self.button_save = Button(text="Save Data")
        # self.button_save.bind(on_press= self.save_data)

        self.carousel = Carousel(direction='right')

        src = ["data/resources/cross.png",
               "data/resources/left.png",
               "data/resources/right.png",
               "data/resources/blank.png"]

        for i in range(len(src)):
            image = AsyncImage(source=src[i], allow_stretch=False)
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

    def change_to_precal(self,*args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'right'

    def start(self,*args):

        if self.stream_flag:
            self.stream_stop()
        else:
            self.stream_start()


    def stream_stop(self):
        self.sm.stop_flag = True
        self.stream_flag = False
        self.sm.join()
        self.button_stream.text = 'Start Streaming'
        self.clock_unscheduler()
        self.save_data()

    def stream_start(self):

        self.load_settings()
        self.generate_stim_list()

        if self.mode == 'playback':

            self.sm = SampleManager('', '', self.channels, mode = self.mode,
                path = self.path_to_file, rec = False)

        elif self.mode == 'simu':
        
            self.sm = SampleManager('', '', self.channels,
                mode = self.mode, rec = True)

        elif self.mode == 'openbci':
        
            self.sm = SampleManager(self.com_port, self.baud_rate, self.channels,
                mode = self.mode, rec = True)

        self.sm.CreateDataProcessing(self.buf_len, self.f_low, self.f_high, self.f_order)
        self.sm.daemon = True  
        self.sm.stop_flag = False
        self.sm.start()
        self.button_stream.text = 'Stop Streaming'
        self.stream_flag = True
        self.clock_scheduler()

    def load_settings(self):

        self.load_session_config()
        self.load_dp_settings()
        self.load_acquisition_settings()
        self.load_cal_settings()


    def get_energy(self, dt):
        if self.stream_flag:
            energy = self.sm.ComputeEnergy()
            if not energy == None:
                self.label_energy.text = "Energy level : {}".format(energy)

    def clock_scheduler(self):
        # Clock.schedule_interval(self.get_energy, 1/6)
        # Clock.schedule_interval(self.save_data, 10)
        Clock.schedule_interval(self.display_epoch, self.end_trial_offset)


    def clock_unscheduler(self):
        Clock.unschedule(self.display_epoch)
        Clock.unschedule(self.get_energy)
        # Clock.unschedule(self.save_data)

    def display_epoch(self, dt):

        if self.epoch_counter < self.n_trials:
            Clock.schedule_once(self.set_pause, self.pause_offset)
            Clock.schedule_once(self.set_cue, self.cue_offset)
            Clock.schedule_once(self.set_blank, self.cue_offset + 1)
        else:
            self.save_data()
            self.stream_stop() 

        
    def set_pause(self, dt):
        self.carousel.index = 0
        self.sm.MarkEvents(0)

    def set_cue(self, dt):

        if self.stim_list[self.epoch_counter] is 1:
            self.carousel.index = 1
            self.sm.MarkEvents(1)

        elif self.stim_list[self.epoch_counter] is 2:
            self.carousel.index = 2
            self.sm.MarkEvents(2)                   

    def set_blank(self, dt):
        self.carousel.index = 3
        self.epoch_counter += 1

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
        self.epoch_start = int(data["epoch_start"])
        self.epoch_end = int(data["epoch_end"])
        self.channels = map(int, data['channels'].split(" "))

    def load_acquisition_settings(self):

        # if os.path.exists("data/rafael/precal_config"):
        with open("data/session/"+ self.session + "/openbci_config.txt", "r") as data_file:    
            data = json.load(data_file)

        self.mode = data["mode"]

        if self.mode == 'openbci':
            self.com_port = data["com_port"]
            self.baud_rate = data["baud_rate"]
            self.ch_labels = data["ch_labels"]

        elif self.mode == 'simu':
            self.ch_labels = data["ch_labels"]

        elif self.mode == 'playback':
            self.path_to_file = data["path_to_file"]

    def load_cal_settings(self):

        # if os.path.exists("data/rafael/precal_config"):
        with open("data/session/"+ self.session + "/cal_config.txt", "r") as data_file:    
            data = json.load(data_file)

        self.n_trials = int(data["n_trials"])
        self.cue_offset = int(data["cue_offset"])
        self.pause_offset = int(data["pause_offset"])
        self.end_trial_offset = int(data["end_trial_offset"])

    def save_data(self):
        PATH_TO_DATA = "data/session/"+ self.session + "/data_cal.txt"
        PATH_TO_EVENTS = "data/session/"+ self.session + "/events_cal.txt"

        print "Saving data"
        self.sm.SaveData(PATH_TO_DATA)
        self.sm.SaveEvents(PATH_TO_EVENTS)

    def generate_stim_list(self):
        self.stim_list =  [random.randrange(1, 3) for _ in range(0, self.n_trials)]
        self.epoch_counter = 0

