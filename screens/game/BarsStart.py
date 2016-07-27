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

    bar_left_level = NumericProperty(0)
    bar_right_level = NumericProperty(0)

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
        self.current_label = int(self.sm.current_playback_label[0])
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

            u = p[1] - .5

            self.U += u

            print 'SELFU:', self.U

            x1 = 100 * (self.U + 1000.) / (2000.)

            print 'x1:', x1

            x2 = 100 - x1

            print x2
            # self.bar_left_level = int(math.floor(p[0] * 100))
            # self.bar_right_level = int(math.floor(p[1] * 100))

            self.bar_left_level = int(math.floor(x1))
            self.bar_right_level = int(math.floor(x2))

    def update_current_label(self, dt):

        label_pos = int(self.sm.current_playback_label[1]) - self.sh.buf_len/2

        previous_label_pos = int(self.sm.previous_playback_label[1]) - self.sh.buf_len/2

        label = int(self.sm.current_playback_label[0])
        previous_label = int(self.sm.previous_playback_label[0])


        tbuff, d = self.sm.GetBuffData()

        # print label_pos, min(tbuff), max(tbuff)
        if (label_pos in tbuff):
            idx = np.where(label_pos == tbuff)[0][0]
            ratio = float(idx) / float(self.sh.buf_len)
            self.label_position = ratio

            if label == 1:
                self.label_color = [1,0,0,1]
            elif label == 2:
                self.label_color = [0,0,1,1]
            else:
                self.label_color = [0,1,1,1]

        elif  previous_label_pos in tbuff:
            idx = np.where(previous_label_pos == tbuff)[0][0]
            ratio = float(idx) / float(self.sh.buf_len)
            self.label_position = ratio

            if previous_label == 1:
                self.label_color = [1,0,0,1]
            elif previous_label == 2:
                self.label_color = [0,0,1,1]
            else:
                self.label_color = [0,1,1,1]

        else:
            self.label_position = -1

    def set_bar_default(self):

        self.bar_left_level = 0
        self.bar_right_level = 0

    def load_approach(self):

        self.ap = Approach()
        self.ap.loadFromPkl(PATH_TO_SESSION + self.sh.name)






    


        