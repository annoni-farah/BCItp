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
    accum_color_left = ListProperty([1,0,0,1])

    inst_prob_right = NumericProperty(0)
    accum_prob_right = NumericProperty(0)
    accum_color_right = ListProperty([0,0,1,1])

    label_on_toggle_button = StringProperty('Start')

    current_label = NumericProperty(None)

    label_position = NumericProperty(-1)

    label_color = ListProperty([0,0,0,1])

    wt = NumericProperty(0.0)

    def __init__ (self, session_header,**kwargs):
        super (BarsStart, self).__init__(**kwargs)
        self.sh = session_header

        self.stream_flag = False

        self.U = 0.0
        self.p = [0,0]

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

        self.sm = SampleManager(self.sh.acq.com_port, self.sh.acq.baud_rate, 
            self.sh.dp.channels, self.sh.dp.buf_len, daisy=self.sh.acq.daisy, 
            mode = self.sh.acq.mode, path = self.sh.acq.path_to_file, 
            labels_path = self.sh.acq.path_to_labels_file, dummy=self.sh.acq.dummy)
        
        self.sm.daemon = True  
        self.sm.stop_flag = False
        self.sm.start()
        self.label_on_toggle_button = 'Stop'
        self.stream_flag = True
        self.clock_scheduler()


    def clock_scheduler(self):
        Clock.schedule_interval(self.get_probs, 1./20.)
        Clock.schedule_interval(self.update_accum_bars, self.sh.game.window_overlap)

        if self.sh.acq.mode == 'simu' and not self.sh.acq.dummy:
            Clock.schedule_interval(self.update_current_label, 1./20.)

    def clock_unscheduler(self):
        Clock.unschedule(self.get_probs)
        Clock.unschedule(self.update_current_label)
        Clock.unschedule(self.update_accum_bars)


    def get_probs(self, dt):

        t, buf = self.sm.GetBuffData()

        if buf.shape[0] == self.sh.dp.buf_len:

            self.p = self.ap.applyModelOnEpoch(buf.T, 'prob')[0]

            if self.sh.game.inst_prob: self.update_inst_bars()

    def update_inst_bars(self):

        p1 = self.p[0]
        p2 = self.p[1]

        u = p1 - p2

        if u > 0:
            self.inst_prob_left = int(math.floor(u * 100))
            self.inst_prob_right = 0
        else:
            self.inst_prob_right = int(math.floor(abs(u) * 100))
            self.inst_prob_left = 0

    def update_accum_bars(self, dt):

        p1 = self.p[0]
        p2 = self.p[1]

        u = p1 - p2

        self.U += u

        U1 = 100 * (self.U + self.sh.game.game_threshold) / (2. * self.sh.game.game_threshold)

        U2 = 100 - U1

        U1_n = int(math.floor(U1))
        U2_n = int(math.floor(U2))

        if U1_n > self.sh.game.warning_threshold:
            self.accum_color_left = [1,1,0,1]
        elif U2_n > self.sh.game.warning_threshold:
            self.accum_color_right = [1,1,0,1]
        else:
            self.accum_color_left = [1,0,0,1]
            self.accum_color_right = [0,0,1,1]

        if U1_n in range(101): self.accum_prob_left = U1_n
        if U2_n in range(101): self.accum_prob_right = U2_n

        self.map_probs(U1, U2)

    def map_probs(self, U1, U2):

        if U1 > 100: self.set_bar_default()
        elif U2 > 100: self.set_bar_default()
        else: pass

            # dont send any cmd

    def set_bar_default(self):

        self.accum_prob_left = 0
        self.accum_prob_right = 0

        self.inst_prob_left = 0
        self.inst_prob_right = 0

        self.U = 0.0

    def update_current_label(self, dt):

        current_label_pos = int(self.sm.current_playback_label[0]) - self.sh.dp.buf_len/2
        current_label = int(self.sm.current_playback_label[1])
        
        next_label_pos = int(self.sm.next_playback_label[0]) - self.sh.dp.buf_len/2
        next_label = int(self.sm.next_playback_label[1])

        self.current_label = current_label

        tbuff, d = self.sm.GetBuffData()

        # print label_pos, min(tbuff), max(tbuff)
        if (next_label_pos in tbuff):
            idx = np.where(next_label_pos == tbuff)[0][0]
            ratio = float(idx) / float(self.sh.dp.buf_len)
            self.label_position = ratio

            if next_label == 1:
                self.label_color = [1,0,0,1]
            elif next_label == 2:
                self.label_color = [0,0,1,1]
            else:
                self.label_color = [0,1,1,1]

        elif  current_label_pos in tbuff:
            idx = np.where(current_label_pos == tbuff)[0][0]
            ratio = float(idx) / float(self.sh.dp.buf_len)
            self.label_position = ratio

            if current_label == 1:
                self.label_color = [1,0,0,1]
            elif current_label == 2:
                self.label_color = [0,0,1,1]
            else:
                self.label_color = [0,1,1,1]

        else:
            self.label_position = -1

    def load_approach(self):

        self.ap = Approach()
        self.ap.loadFromPkl(PATH_TO_SESSION + self.sh.info.name)





    


        