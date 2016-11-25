# DEPENDENCIES-------------------------
# Generic:
import math
import random
import time
import numpy as np

# Project's:
from utils.sample_manager import SampleManager
from utils.standards import PATH_TO_SESSION
from signal_processing.approach import Approach
from signal_processing.handler import save_matrix_as_txt

# KIVY modules:
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.core.window import Window


######################################################################


class TargetStart(Screen):

    inst_prob_left = NumericProperty(0)
    accum_prob_left = NumericProperty(0)
    accum_color_left = ListProperty([0, 0, 1, 1])

    inst_prob_right = NumericProperty(0)
    accum_prob_right = NumericProperty(0)
    accum_color_right = ListProperty([0, 0, 1, 1])

    label_on_toggle_button = StringProperty('Start')

    game = ObjectProperty(None)

    current_label = NumericProperty(None)

    label_color = ListProperty([0, 0, 0, 1])

    wt = NumericProperty(0.0)

    def __init__(self, session_header, **kwargs):
        super(TargetStart, self).__init__(**kwargs)
        self.sh = session_header

        self.U = 0.0
        self.p = [0, 0]

        self.stream_flag = False
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
        if self.sh.game.keyb_enable:
            self.game.keyb_enable = False

        else:
            self.sm.stop_flag = True
            self.sm.join()
            self.clock_unscheduler()
            self.set_bar_default()

        self.stream_flag = False
        self.label_on_toggle_button = 'Start'
        self.game.stop()

        res = GameResultsPopup(self.sh, self.game.res_h)
        res.open()

    def stream_start(self):
        self.load_approach()

        if self.sh.game.keyb_enable:
            self.game.keyb_enable = True

        else:
            self.sm = SampleManager(self.sh.acq.com_port,
                                    self.sh.dp.buf_len,
                                    daisy=self.sh.acq.daisy,
                                    mode=self.sh.acq.mode,
                                    path=self.sh.acq.path_to_file,
                                    labels_path=self.sh.acq.path_to_labels_file,
                                    dummy=self.sh.acq.dummy)
            self.sm.daemon = True
            self.sm.stop_flag = False
            self.sm.start()
            self.clock_scheduler()

        self.stream_flag = True
        self.label_on_toggle_button = 'Stop'
        self.game.set_player_speed(self.sh.game.forward_speed)
        self.game.setup()
        self.game.start(None)

    def clock_scheduler(self):
        Clock.schedule_interval(self.get_probs, 1. / 20.)
        Clock.schedule_interval(self.update_accum_bars,
                                self.sh.game.window_overlap)
        if self.sh.acq.mode == 'simu' and not self.sh.acq.dummy:
            Clock.schedule_interval(self.update_current_label, 1. / 20.)

    def clock_unscheduler(self):
        Clock.unschedule(self.get_probs)
        Clock.unschedule(self.update_current_label)
        Clock.unschedule(self.update_accum_bars)

    def get_probs(self, dt):

        t, buf = self.sm.GetBuffData()

        if buf.shape[0] == self.sh.dp.buf_len:

            self.p = self.ap.applyModelOnEpoch(buf.T, 'prob')[0]

            if self.sh.game.inst_prob:
                self.update_inst_bars()

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

        U1 = 100 * (self.U + self.sh.game.game_threshold) / \
            (2. * self.sh.game.game_threshold)

        U2 = 100 - U1

        U1_n = int(math.floor(U1))
        U2_n = int(math.floor(U2))

        if U1_n > self.sh.game.warning_threshold:
            self.accum_color_left = [1, 1, 0, 1]
        elif U2_n > self.sh.game.warning_threshold:
            self.accum_color_right = [1, 1, 0, 1]
        else:
            self.accum_color_left = [1, 0, 0, 1]
            self.accum_color_right = [0, 0, 1, 1]

        if U1_n in range(101):
            self.accum_prob_left = U1_n
        if U2_n in range(101):
            self.accum_prob_right = U2_n

        self.map_probs(U1, U2)

    def map_probs(self, U1, U2):

        # print self.game.direction

        if U1 > 100:
            self.game.set_direction(-1)
            self.set_bar_default()
            # print self.game.direction

            return 0, 0

        elif U2 > 100:
            self.game.set_direction(1)
            self.set_bar_default()
            # print self.game.direction

            return 0, 0

        else:
            return U1, U2
            # dont send any cmd

    def set_bar_default(self):

        self.accum_prob_left = 0
        self.accum_prob_right = 0

        self.inst_prob_left = 0
        self.inst_prob_right = 0

        self.U = 0.0

    def update_current_label(self, dt):

        current_label = int(self.sm.current_playback_label[1])
        self.current_label = current_label

    def load_approach(self):

        self.ap = Approach()
        self.ap.loadFromPkl(PATH_TO_SESSION + self.sh.info.name)


class Game(Widget):

    player = ObjectProperty(None)
    target = ObjectProperty(None)

    vel = NumericProperty(1)

    keyb_enable = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(None, self)
        if not self._keyboard:
            return

        self.direction = 'up'

        self.direction_list = ['left', 'up', 'right', 'down']
        self.direction_idx = 1

        self.on_flag = False

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.set_direction(-1)
        elif keycode[1] == 'right':
            self.set_direction(1)
        else:
            return False

        return True

    def set_player_speed(self, speed):

        self.forward_speed = speed

    def set_positions(self):

        max_width = int(self.parent.width)
        max_height = int(self.parent.height)

        self.target.pos = (random.randint(0, max_width),
                           random.randint(0, max_height))

        self.player.pos = self.center

    def setup(self):
        self.res_h = [0]
        if self.keyb_enable:
            self._keyboard.bind(on_key_down=self.on_keyboard_down)

    def start(self, dt):

        self.target.t_color = [1, 1, 0, 1]

        self.set_positions()

        self.on_flag = True

        Clock.schedule_interval(self.check_if_won, 1. / 5.)
        Clock.schedule_interval(self.move_player, self.forward_speed)

        self.time_start = time.time()

    def stop(self):
        # unbind keyboard even if it wasnt before
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.on_flag = False
        Clock.unschedule(self.check_if_won)
        Clock.unschedule(self.move_player)

    def check_if_won(self, dt):
        if self.player.collide_widget(self.target):
            self.target.t_color = [0, 1, 0, 1]
            Clock.schedule_once(self.start, 2)
            self.time_stop = time.time()
            self.res_h.append(self.time_stop - self.time_start)
            Clock.unschedule(self.check_if_won)
            Clock.unschedule(self.move_player)

    def set_direction(self, direction):

        # print 'changing by:', direction

        if (self.direction_idx == 0) and (direction == -1):
            self.direction_idx = 3
        elif (self.direction_idx == 3) and (direction == 1):
            self.direction_idx = 0
        else:
            self.direction_idx += direction

        self.direction = self.direction_list[self.direction_idx]
        self.move_player(None)

    def move_player(self, dt):
        l = self.player.width
        p0 = self.player.pos[0]
        p1 = self.player.pos[1]

        # print 'moving to:', self.direction

        if self.direction == 'right':
            x0 = p0
            y0 = p1 + l
            x1 = p0 + l
            y1 = p1 + l / 2
            x2 = p0
            y2 = p1
            if self.player.center_x <= int(self.parent.width) - 15:
                self.player.pos[0] += self.vel

        elif self.direction == 'left':
            x0 = p0 + l
            y0 = p1
            x1 = p0
            y1 = p1 + l / 2
            x2 = p0 + l
            y2 = p1 + l

            if self.player.center_x >= 15:
                self.player.pos[0] -= self.vel

        elif self.direction == 'up':
            x0 = p0
            y0 = p1
            x1 = p0 + l / 2
            y1 = p1 + l
            x2 = p0 + l
            y2 = p1

            if self.player.center_y <= int(self.parent.height) - 15:
                self.player.pos[1] += self.vel

        elif self.direction == 'down':
            x0 = p0 + l
            y0 = p1 + l
            x1 = p0 + l / 2
            y1 = p1
            x2 = p0
            y2 = p1 + l

            if self.player.center_y >= 15:
                self.player.pos[1] -= self.vel

        self.player.points = [x0, y0, x1, y1, x2, y2]


class GamePlayer(Widget):
    points = ListProperty([0] * 6)


class GameTarget(Widget):
    t_color = ListProperty([1, 1, 0, 1])


class GameResultsPopup(Popup):

    res = ListProperty([0])

    hits = NumericProperty(0)

    def __init__(self, sh, results, **kwargs):
        super(GameResultsPopup, self).__init__(**kwargs)

        self.sh = sh

        if len(results) > 1:
            self.res = results[1:]
            self.hits = len(self.res)

    def save_results(self, game_name):
        path = PATH_TO_SESSION + self.sh.info.name + \
            '/' + 'game_results_' + game_name + '.npy'

        r = np.array(self.res)
        save_matrix_as_txt(r, path, mode='w')
