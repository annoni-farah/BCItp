############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty, \
                            ListProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock



# KV file:
Builder.load_file('screens/cal/calstart.kv')

# Generic:
import random
import json
import os

# Project's:
from standards import *
from approach import Approach
from SampleManager import *

######################################################################


class CalStart(Screen):

    src = ["data/resources/cross.png", \
       "data/resources/left.png", \
       "data/resources/right.png", \
       "data/resources/blank.png"]

    fig_list = ListProperty(src)
    button_stream = StringProperty('Start Streaming')

    carousel = ObjectProperty(None)

# layout
    def __init__ (self, session_header,**kwargs):
        super (CalStart, self).__init__(**kwargs)

        self.sh = session_header
        self.stream_flag = False

    def change_to_cal(self,*args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'right'

    def toggle_stream(self,*args):

        if self.stream_flag:
            self.stream_stop()
        else:
            self.stream_start()

    def stream_stop(self):
        self.sm.stop_flag = True
        self.stream_flag = False
        self.sm.join()
        self.button_stream = 'Start Streaming'
        self.clock_unscheduler()
        self.save_data()

    def stream_start(self):

        self.generate_stim_list()
        self.sm = SampleManager(self.sh.acq.com_port, self.sh.acq.baud_rate, 
            self.sh.dp.channels, self.sh.dp.buf_len, daisy=self.sh.acq.daisy, 
            mode = self.sh.acq.mode, dummy=self.sh.acq.dummy)
        self.sm.daemon = True  
        self.sm.stop_flag = False
        self.sm.start()
        self.button_stream = 'Stop Streaming'
        self.stream_flag = True
        self.clock_scheduler()

    def clock_scheduler(self):
        Clock.schedule_interval(self.display_epoch, self.sh.cal.end_trial_offset)


    def clock_unscheduler(self):
        Clock.unschedule(self.display_epoch)

    def display_epoch(self, dt):

        if self.epoch_counter < self.sh.cal.n_trials:
            Clock.schedule_once(self.set_pause, self.sh.cal.pause_offset)
            Clock.schedule_once(self.set_cue, self.sh.cal.cue_offset)
            Clock.schedule_once(self.set_blank, self.sh.cal.cue_offset + 1)
        else:
            self.stream_stop() 

        
    def set_pause(self, dt):
        # os.system('play --no-show-progress --null --channels 1 synth %s sine %f &' % ( 0.3, 500))
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
        self.sm.SaveData(self.sh.cal.data_cal_path)
        self.sm.SaveEvents(self.sh.cal.events_cal_path)

    def generate_stim_list(self):
        self.stim_list =  [random.randrange(1, 3) for _ in range(0, self.sh.cal.n_trials)]
        self.epoch_counter = 0

