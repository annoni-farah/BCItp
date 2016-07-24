############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder

# KV file:
Builder.load_file('screens/game/barsstart.kv')

# Generic:
import math

# Project's:
from SampleManager import *
from standards import *
from approach import Approach
######################################################################

class BarsStart(Screen):

    bar_left_level = NumericProperty(0)
    bar_right_level = NumericProperty(0)

    def __init__ (self, session_header,**kwargs):
        super (BarsStart, self).__init__(**kwargs)
        self.sh = session_header

        self.stream_flag = False

    # BUTTON CALLBACKS    
    # ----------------------
    def change_to_game(self,*args):

        self.manager.current = 'GameMenu'
        self.manager.transition.direction = 'right'

    def toogle_stream(self,*args):
        if self.stream_flag:
            self.stream_stop()
        else:
            self.stream_start()

    # ----------------------

    def stream_stop(self):
        self.sm.stop_flag = True
        self.stream_flag = False
        self.sm.join()
        self.button_stream.text = 'Start Streaming'
        self.clock_unscheduler()
        self.set_bar_default()

    def stream_start(self):
        self.load_approach()
        self.sm = SampleManager(self.sh.com_port, self.sh.baud_rate, self.sh.channels,
            self.sh.buf_len, daisy=self.sh.daisy, mode = self.sh.mode, path = self.sh.path_to_file)
        self.sm.daemon = True  
        self.sm.stop_flag = False
        self.sm.start()
        self.button_stream.text = 'Stop Streaming'
        self.stream_flag = True
        self.clock_scheduler()


    def clock_scheduler(self):
        Clock.schedule_interval(self.get_probs, 1/2)

    def clock_unscheduler(self):
        Clock.unschedule(self.get_probs)


    def get_probs(self, dt):

        t, buf = self.sm.GetBuffData()

        if buf.shape[0] == self.sh.buf_len:

            p = self.ap.applyModelOnEpoch(buf.T, 'prob')[0]

            self.bar_left_level = int(math.floor(p[0] * 100))
            self.bar_right_level = int(math.floor(p[1] * 100))

    def set_bar_default(self):

        self.bar_left_level = 0
        self.bar_right_level = 0

    def load_approach(self):

        self.ap = Approach()
        self.ap.loadFromPkl(PATH_TO_SESSION + self.sh.name)






    


        