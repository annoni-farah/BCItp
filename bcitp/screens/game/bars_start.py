# DEPENDENCIES-------------------------
# Generic:
import math
import os
import collections

# Project's:
from bcitp.handlers.data_handler import DataHandler
from bcitp.utils.standards import PATH_TO_SESSION
from bcitp.signal_processing.approach import Approach
from bcitp.signal_processing.handler import save_matrix_as_txt

# KIVY modules:
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup


######################################################################


class BarsStart(Screen):

    inst_prob_left = NumericProperty(0)
    accum_prob_left = NumericProperty(0)
    accum_color_left = ListProperty([1, 0, 0, 1])

    inst_prob_right = NumericProperty(0)
    accum_prob_right = NumericProperty(0)
    accum_color_right = ListProperty([0, 0, 1, 1])

    label_on_toggle_button = StringProperty('Start')

    current_label = NumericProperty(None)

    label_color = ListProperty([0, 0, 0, 1])

    wt = NumericProperty(0.0)

    def __init__(self, session_header, **kwargs):
        super(BarsStart, self).__init__(**kwargs)
        self.sh = session_header

        self.stream_flag = False

        self.U1 = 0.0
        self.U2 = 0.0

        self.p = [0, 0]

    # BUTTON CALLBACKS
    # ----------------------
    def change_to_game(self, *args):

        self.manager.current = 'GameMenu'
        self.manager.transition.direction = 'right'

    def toogle_stream(self, *args):
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

        res = GameDataPopup(self.sh, self.sm.all_data)
        res.open()

    def stream_start(self):
        self.load_approach()

        TTA = 5.
        increment = 25.
        ABUF_LEN = TTA * self.sh.acq.sample_rate / increment
        self.delta_ref = self.ap.accuracy * \
            TTA / (increment / self.sh.acq.sample_rate)

        self.U1_local = collections.deque(maxlen=ABUF_LEN)
        self.U2_local = collections.deque(maxlen=ABUF_LEN)

        self.sm = DataHandler(self.sh.acq.com_port,
                                self.sh.dp.buf_len,
                                daisy=self.sh.acq.daisy,
                                mode=self.sh.acq.mode,
                                path=self.sh.acq.path_to_file,
                                labels_path=self.sh.acq.path_to_labels_file,
                                dummy=self.sh.acq.dummy)

        self.sm.daemon = True
        self.sm.stop_flag = False
        self.sm.start()
        self.label_on_toggle_button = 'Stop'
        self.stream_flag = True
        self.clock_scheduler()

    def clock_scheduler(self):
        Clock.schedule_interval(self.get_probs, 1. / 20.)
        Clock.schedule_interval(self.update_accum_bars,
                                self.sh.game.window_overlap)

        if (self.sh.acq.mode == 'simu' and
                not self.sh.acq.dummy and
                not self.sh.acq.path_to_labels_file == ''):
            Clock.schedule_interval(self.update_current_label, 1. / 20.)

    def clock_unscheduler(self):
        Clock.unschedule(self.get_probs)
        Clock.unschedule(self.update_current_label)
        Clock.unschedule(self.update_accum_bars)

    def get_probs(self, dt):

        t, buf = self.sm.GetBuffData()

        if buf.shape[0] == self.sh.dp.buf_len:

            self.p = self.ap.classify_epoch(buf.T, 'prob')[0]

            if self.sh.game.inst_prob:
                self.update_inst_bars()

    def update_inst_bars(self):

        if self.p is None:
            return

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

        if self.p is None:
            return

        p1 = self.p[0]
        p2 = self.p[1]

        u = p1 - p2

        if u >= 0:
            u1 = 1
            u2 = 0
        else:
            u1 = 0
            u2 = 1

        self.U1 = self.U1 + u1
        self.U2 = self.U2 + u2
        self.U1_local.append(self.U1)
        self.U2_local.append(self.U2)

        delta1 = self.U1_local[-1] - self.U1_local[0]
        delta2 = self.U2_local[-1] - self.U2_local[0]

        BAR1 = 100 * (delta1 / self.delta_ref)
        BAR2 = 100 * (delta2 / self.delta_ref)

        BAR1_n = int(math.floor(BAR1))
        BAR2_n = int(math.floor(BAR2))

        if BAR1_n < 100:
            self.accum_prob_left = BAR1_n
        if BAR2_n < 100:
            self.accum_prob_right = BAR2_n

        self.map_probs(BAR1, BAR2)

    def map_probs(self, BAR1, BAR2):

        if BAR1 > 100:
            os.system(self.sh.game.action_cmd1)
            self.set_bar_default()
        elif BAR2 > 100:
            os.system(self.sh.game.action_cmd2)
            self.set_bar_default()
        else:
            pass
            # dont send any cmd

    def set_bar_default(self):

        self.accum_prob_left = 0
        self.accum_prob_right = 0

        self.inst_prob_left = 0
        self.inst_prob_right = 0

        self.U1_local.clear()
        self.U2_local.clear()

    def update_current_label(self, dt):

        self.current_label = self.sm.current_cmd

    def load_approach(self):

        self.ap = Approach()
        self.ap.load_pkl(PATH_TO_SESSION + self.sh.info.name)


class GameDataPopup(Popup):

    def __init__(self, sh, data, **kwargs):
        super(GameDataPopup, self).__init__(**kwargs)

        self.sh = sh
        self.data = data

    def save_data(self, game_name):
        path = PATH_TO_SESSION + self.sh.info.name + \
            '/' + 'bar_data_' + game_name + '.npy'

        save_matrix_as_txt(self.data, path, mode='w')
