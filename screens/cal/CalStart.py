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

        box2.add_widget(self.carousel)
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

        self.generate_stim_list()
        self.sm = SampleManager(self.sh.com_port, self.sh.baud_rate, self.sh.channels, self.sh.buf_len,
            daisy=self.sh.daisy, mode = self.sh.mode)
        self.sm.daemon = True  
        self.sm.stop_flag = False
        self.sm.start()
        self.button_stream.text = 'Stop Streaming'
        self.stream_flag = True
        self.clock_scheduler()

    def clock_scheduler(self):
        Clock.schedule_interval(self.display_epoch, self.sh.end_trial_offset)


    def clock_unscheduler(self):
        Clock.unschedule(self.display_epoch)

    def display_epoch(self, dt):

        if self.epoch_counter < self.sh.n_trials:
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f &' % ( 0.3, 500))
            Clock.schedule_once(self.set_pause, self.sh.pause_offset)
            Clock.schedule_once(self.set_cue, self.sh.cue_offset)
            Clock.schedule_once(self.set_blank, self.sh.cue_offset + 1)
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

    def save_data(self):

        print "Saving data"
        self.sm.SaveData(self.sh.data_cal_path)
        self.sm.SaveEvents(self.sh.events_cal_path)

    def generate_stim_list(self):
        self.stim_list =  [random.randrange(1, 3) for _ in range(0, self.sh.n_trials)]
        self.epoch_counter = 0

