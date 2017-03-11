# DEPENDENCIES ------------------------
# Generic:
import math
from time import sleep
import numpy as np
import time
import collections

# Project's:
from bcitp.utils.sample_manager import SampleManager
from bcitp.utils.standards import PATH_TO_SESSION
from bcitp.signal_processing.approach import Approach
from bcitp.signal_processing.handler import save_matrix_as_txt

# KIVY modules:
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup


DRONE_VEL = 1
K = 1
I = 1

D_TO_TARGET = 10

TARGET_POS_ARR = [[0, 0], [-20, 0], [-20, 20], [20 + D_TO_TARGET, 20]]  # simu1
CMD_LIST = [1, 2, 2]

# TARGET_POS_ARR = [[0, 0], [20, 0], [20, 20], [-20, 20]] # simu2
# CMD_LIST = [2, 1, 1]

# TARGET_POS_ARR = [[0, 20], [-20, 20], [-20, 0]] # simu3
# CMD_LIST = [1, 1]
######################################################################


class DroneStart(Screen):
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
        super(DroneStart, self).__init__(**kwargs)
        self.sh = session_header

        self.stream_flag = False
        self.p = None

        self.U1 = 0.0
        self.U2 = 0.0

    # BUTTON CALLBACKS
    # ----------------------
    def change_to_drone(self, *args):

        self.manager.current = 'DroneMenu'
        self.manager.transition.direction = 'right'

    def toogle_stream(self, *args):
        if self.stream_flag:
            self.stream_stop()
        else:
            self.stream_start()

    # ----------------------

    def start_drone(self):
        # Hardware:
        from bcitp.hardware.ardrone_ros import ARDrone
        self.drone = ARDrone()

    def stream_stop(self):
        self.sm.stop_flag = True
        self.stream_flag = False
        self.sm.join()
        self.label_on_toggle_button = 'Start'
        self.clock_unscheduler()
        self.set_bar_default()
        # self.save_results()
        self.drone.stop()
        self.drone.land()
        self.drone.reset()
        game_time = time.time() - self.game_start_time
        results = np.array([(self.pos_history), (game_time)])
        res = DroneResultsPopup(self.sh, results, self.sm.all_data)
        res.open()

        # global I
        # if self.bad_run:
        #     res.save_results('run' + str(I) + 'bad')
        # else:
        #     res.save_results('run' + str(I))
        # I += 1
        # if I < 20:
        #     sleep(4)
        #     self.stream_start()

    def stream_start(self):
        self.lock_check_pos = False
        self.drone.stop()
        self.bad_run = False
        self.cmd_list = iter(CMD_LIST)
        self.target_pos_arr = iter(TARGET_POS_ARR)
        self.update_target_area()

        self.load_approach()

        TTA = 10.
        ABUF_LEN = TTA * self.sh.acq.sample_rate / self.sh.game.window_overlap
        self.delta_ref = self.ap.accuracy * ABUF_LEN
        self.U1_local = collections.deque(maxlen=ABUF_LEN)
        self.U2_local = collections.deque(maxlen=ABUF_LEN)

        self.sm = SampleManager(self.sh.acq.com_port,
                                self.sh.dp.buf_len, daisy=self.sh.acq.daisy,
                                mode=self.sh.acq.mode,
                                path=self.sh.acq.path_to_file,
                                labels_path=self.sh.acq.path_to_labels_file,
                                dummy=self.sh.acq.dummy)

        self.sm.daemon = True
        self.sm.stop_flag = False
        self.sm.start()
        self.label_on_toggle_button = 'Stop'
        self.stream_flag = True
        self.pos_history = np.array([0, 0])
        self.clock_scheduler()
        self.drone.takeoff()
        self.game_start_time = time.time()

    def clock_scheduler(self):
        Clock.schedule_once(self.move_drone_forward, 2)
        Clock.schedule_interval(self.get_probs, 1. / 20.)
        Clock.schedule_interval(self.update_accum_bars,
                                float(self.sh.game.window_overlap) / self.sh.acq.sample_rate)
        Clock.schedule_interval(self.store_pos, .2)
        Clock.schedule_interval(self.check_pos, 1. / 10.)

        if self.sh.acq.mode == 'simu' and not self.sh.acq.dummy:
            pass
            Clock.schedule_interval(self.update_current_label, 1. / 5.)

    def clock_unscheduler(self):
        Clock.unschedule(self.get_probs)
        Clock.unschedule(self.update_current_label)
        Clock.unschedule(self.update_accum_bars)
        Clock.unschedule(self.store_pos)
        Clock.unschedule(self.check_pos)

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

        if u >= 0:
            u = 1
        else:
            u = -1

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

        print u

        if u >= 0:
            u1 = 1
            u2 = 0
        elif u < 0:
            u1 = 0
            u2 = 1
        else:
            return

        print u1, u2

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

    def map_probs(self, U1, U2):

        if (U1 > 100) or (U2 > 100):
            self.drone.stop()
            self.set_bar_default()
            # self.sm.clear_buffer()
            self.sm.current_cmd = 0
            Clock.schedule_once(self.move_drone_forward, 2)
            if U1 > 100:
                self.drone.set_direction('left')
            else:
                self.drone.set_direction('right')

            self.update_target_area()
            self.lock_check_pos = False
        elif self.sm.current_cmd == 0:
            if U1 > U2:
                self.sm.winning = 1
            else:
                self.sm.winning = 2
            # dont send any cmd

    def move_drone_forward(self, dt):
        self.drone.set_forward_vel(DRONE_VEL)

    def set_bar_default(self):

        self.accum_prob_left = 0
        self.accum_prob_right = 0

        self.inst_prob_left = 0
        self.inst_prob_right = 0

        self.p = None

        self.U1_local.clear()
        self.U2_local.clear()

    def update_current_label(self, dt):

        self.current_label = self.sm.current_cmd

    def load_approach(self):

        self.ap = Approach()
        self.ap.load_pkl(PATH_TO_SESSION + self.sh.info.name)

    def store_pos(self, dt):
        new = [self.drone.pos_x, self.drone.pos_y]
        self.pos_history = np.vstack([self.pos_history, new])

    def check_pos(self, dt):
        if self.lock_check_pos:
            # print('locked')
            return

        pos = [self.drone.pos_x, self.drone.pos_y]
        target_area = self.target_area
        if ((target_area[0] < pos[0] < target_area[2]) and
                (target_area[1] < pos[1] < target_area[3])):
            print('entrou na area')
            try:
                self.sm.current_cmd = next(self.cmd_list)

                # self.sm.clear_buffer()
                # self.sm.jump_playback_data()
                self.set_bar_default()
                self.lock_check_pos = True

            except StopIteration:
                self.stream_stop()

        else:
            if (abs(pos[0]) > 35 or abs(pos[1]) > 35):
                self.bad_run = True
                self.stream_stop()

    def update_target_area(self):
        try:
            target_pos = next(self.target_pos_arr)

            targ_yaw = self.drone.target_yaw

            if targ_yaw == 270:
                self.target_area = [
                    target_pos[0] - 100,
                    target_pos[1] - D_TO_TARGET,
                    target_pos[0] + 100,
                    target_pos[1] + 100,
                ]

            elif targ_yaw == 360 or targ_yaw == 0:
                self.target_area = [
                    target_pos[0] - 100,
                    target_pos[1] - 100,
                    target_pos[0] + D_TO_TARGET,
                    target_pos[1] + 100,
                ]

            if targ_yaw == 90:
                self.target_area = [
                    target_pos[0] - 100,
                    target_pos[1] - 100,
                    target_pos[0] + 100,
                    target_pos[1] + D_TO_TARGET,
                ]

            if targ_yaw == 180:
                self.target_area = [
                    target_pos[0] - D_TO_TARGET,
                    target_pos[1] - 100,
                    target_pos[0] + 100,
                    target_pos[1] + 100,
                ]

        except StopIteration:
            self.stream_stop()


class DroneResultsPopup(Popup):

    def __init__(self, sh, results, data, **kwargs):
        super(DroneResultsPopup, self).__init__(**kwargs)

        self.sh = sh
        self.res = results
        self.data = data

    def save_results(self, game_name):
        path_res = (PATH_TO_SESSION + self.sh.info.name +
                    '/' + 'game_results_' + game_name + '.npy')

        path_data = (PATH_TO_SESSION + self.sh.info.name +
                     '/' + 'game_data_' + game_name + '.npy')

        r = np.array(self.res)
        save_matrix_as_txt(r, path_res, mode='w')
        save_matrix_as_txt(r, path_data, mode='w')
