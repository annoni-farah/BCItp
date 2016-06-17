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

import os

from standards import *

class CalStart(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (CalStart, self).__init__(**kwargs)

        self.sh = session_header

        box = BoxLayout(size_hint_x=1, size_hint_y=1,padding=10, spacing=10, orientation='vertical')

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='vertical')
        box2 = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='vertical')

        button_back = Button(text="Back", size = BUTTON_SIZE)
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
        
            self.sm = SampleManager('', '', self.channels, daisy=self.daisy,
                mode = self.mode, rec = True)

        elif self.mode == 'openbci':
        
            self.sm = SampleManager(self.com_port, self.baud_rate, self.channels,
                daisy=self.daisy, mode = self.mode, rec = True)

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
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f &' % ( 0.3, 500))

        if self.epoch_counter < self.n_trials:
            Clock.schedule_once(self.set_pause, self.pause_offset)
            Clock.schedule_once(self.set_cue, self.cue_offset)
            Clock.schedule_once(self.set_blank, self.cue_offset + 1)
        else:
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
        self.session = self.sh.name

    def load_dp_settings(self):

        self.buf_len, self.f_low, self.f_high, \
            self.f_order, self.channels = self.sh.getDataProcessingConfig()

    def load_acquisition_settings(self):

        self.mode, self.com_port, self.baud_rate, \
            self.ch_labels, self.path_to_file, self.fs, self.daisy = self.sh.getAcquisitionConfig()

    def load_cal_settings(self):

        self.n_trials, self.cue_offset, self.pause_offset, \
            self.end_trial_offset = self.sh.getCalibrationConfig()

    def save_data(self):
        PATH_TO_DATA = "data/session/"+ self.session + "/data_cal.txt"
        PATH_TO_EVENTS = "data/session/"+ self.session + "/events_cal.txt"

        print "Saving data"
        self.sm.SaveData(PATH_TO_DATA)
        self.sm.SaveEvents(PATH_TO_EVENTS)

    def generate_stim_list(self):
        self.stim_list =  [random.randrange(1, 3) for _ in range(0, self.n_trials)]
        self.epoch_counter = 0

