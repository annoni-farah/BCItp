############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.lang import Builder

# KV file:
Builder.load_file('screens/game/barsstart.kv')

# Generic:
import math
import numpy as np

# Project's:
from SampleManager import *
from standards import *
from approach import Approach
######################################################################

class BarsStart(Screen):

    inst_prob_left = NumericProperty(0)
    accum_prob_left = NumericProperty(0)

    inst_prob_right = NumericProperty(0)
    accum_prob_right = NumericProperty(0)

    label_on_toggle_button = StringProperty('Start')

    current_label = NumericProperty(None)

    label_position = NumericProperty(-1)

    label_color = ListProperty([0,0,0,1])

    def __init__ (self, session_header,**kwargs):
        super (BarsStart, self).__init__(**kwargs)
        self.sh = session_header

        self.stream_flag = False

        self.U = 0.0

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
        self.label_on_toggle_button = 'Start'
        self.clock_unscheduler()
        self.set_bar_default()

    def stream_start(self):
        self.load_approach()
        self.sm = SampleManager(self.sh.com_port, self.sh.baud_rate, self.sh.channels,
            self.sh.buf_len, daisy=self.sh.daisy, mode = self.sh.mode, path = self.sh.path_to_file,
            labels_path = self.sh.path_to_labels_file)
        self.sm.daemon = True  
        self.sm.stop_flag = False
        self.sm.start()
        self.label_on_toggle_button = 'Stop'
        self.stream_flag = True
        self.clock_scheduler()


    def clock_scheduler(self):
        Clock.schedule_interval(self.get_probs, 1/2)
        Clock.schedule_interval(self.update_current_label, 1/8)

    def clock_unscheduler(self):
        Clock.unschedule(self.get_probs)
        Clock.unschedule(self.update_current_label)


    def get_probs(self, dt):

        t, buf = self.sm.GetBuffData()

        if buf.shape[0] == self.sh.buf_len:

            p = self.ap.applyModelOnEpoch(buf.T, 'prob')[0]

            u = p[0] - .5

            self.U += u
 
            U1 = 100 * (self.U + 1000.) / (2000.)

            U2 = 100 - U1

            # print U2
            self.inst_prob_left = int(math.floor(p[0] * 100))
            self.inst_prob_right = int(math.floor(p[1] * 100))

            if U1 > 100:
                U1 = 100
                U2 = 0
            elif U2 > 100:
                U2 = 100
                U1 = 0

            self.accum_prob_left = int(math.floor(U1))
            self.accum_prob_right = int(math.floor(U2))

            self.map_prob([U1, U2])

    def map_prob(self, prob):

        U1 = prob[0]

        if (U1) > 70:
            self.set_bar_default()
        elif  U1 < 30:
            self.set_bar_default()
        else:
            pass
            # dont send any cmd

    def update_current_label(self, dt):

        current_label_pos = int(self.sm.current_playback_label[1]) - self.sh.buf_len/2
        current_label = int(self.sm.current_playback_label[0])
        
        next_label_pos = int(self.sm.next_playback_label[1]) - self.sh.buf_len/2
        next_label = int(self.sm.next_playback_label[0])

        self.current_label = current_label

        tbuff, d = self.sm.GetBuffData()

        # print label_pos, min(tbuff), max(tbuff)
        if (next_label_pos in tbuff):
            idx = np.where(next_label_pos == tbuff)[0][0]
            ratio = float(idx) / float(self.sh.buf_len)
            self.label_position = ratio

            if next_label == 1:
                self.label_color = [1,0,0,1]
            elif next_label == 2:
                self.label_color = [0,0,1,1]
            else:
                self.label_color = [0,1,1,1]

        elif  current_label_pos in tbuff:
            idx = np.where(current_label_pos == tbuff)[0][0]
            ratio = float(idx) / float(self.sh.buf_len)
            self.label_position = ratio

            if current_label == 1:
                self.label_color = [1,0,0,1]
            elif current_label == 2:
                self.label_color = [0,0,1,1]
            else:
                self.label_color = [0,1,1,1]

        else:
            self.label_position = -1

    def set_bar_default(self):

        self.accum_prob_left = 0
        self.accum_prob_right = 0

        self.inst_prob_left = 0
        self.inst_prob_right = 0

        self.U = 0.0

    def load_approach(self):

        self.ap = Approach()
        self.ap.loadFromPkl(PATH_TO_SESSION + self.sh.name)






    


        