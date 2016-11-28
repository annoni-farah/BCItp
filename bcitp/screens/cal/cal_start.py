# DEPENDENCIES -------------------------
# Generic:
import random
import os
import time
import threading
import numpy as np

# Project's:
from bcitp.utils.sample_manager import SampleManager

# KIVY modules:
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    ListProperty
from kivy.clock import Clock
from kivy.garden.bar import Bar

######################################################################


class CalStart(Screen):

    src = ["bcitp/screens/resources/cross.png",
           "bcitp/screens/resources/left.png",
           "bcitp/screens/resources/right.png",
           "bcitp/screens/resources/blank.png",
           "bcitp/screens/resources/break.png"]

    fig_list = ListProperty(src)
    button_stream = StringProperty('Start Streaming')

    carousel = ObjectProperty(None)
    inst_prob_left = NumericProperty(0)
    inst_prob_right = NumericProperty(0)

    accum_color_left = ListProperty([1, 0, 0, 1])
    accum_color_right = ListProperty([0, 0, 1, 1])


# layout
    def __init__(self, session_header, **kwargs):
        super(CalStart, self).__init__(**kwargs)

        self.sh = session_header

        self.carousel.index = 3

        self.stream_flag = False

    def change_to_cal(self, *args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'right'

    def toggle_stream(self, *args):

        if self.stream_flag:
            self.stream_stop()
            self.stop_stimulus()
        else:
            self.stream_start()

    def stream_start(self):

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
        self.button_stream = 'Stop Streaming'
        self.stream_flag = True
        self.start_stimulus()
        self.set_bar_default()

    def stream_stop(self):
        self.sm.stop_flag = True
        self.stream_flag = False
        self.sm.join()
        self.button_stream = 'Start Streaming'
        self.save_data()
        self.set_bar_default()

    def start_stimulus(self):
        self.epoch_counter = 0
        self.run_counter = 0

        self.generate_stim_list()
        self.start_run(None)

    def stop_stimulus(self):
        Clock.unschedule(self.display_epoch)
        Clock.unschedule(self.start_run)
        Clock.unschedule(self.set_pause)
        Clock.unschedule(self.set_cue)
        Clock.unschedule(self.set_blank)
        self.carousel.index = 3

    def start_run(self, dt):
        self.run_epoch_counter = 0
        self.carousel.index = 3
        Clock.schedule_interval(
            self.display_epoch, self.sh.cal.end_trial_offset)

    def stop_run(self):
        self.stop_stimulus()
        self.run_counter += 1

        if self.run_counter < self.sh.cal.n_runs:
            Clock.schedule_once(self.start_run, self.sh.cal.runs_interval)
            self.carousel.index = 4
        else:
            self.stream_stop()
            self.stop_stimulus()

    def display_epoch(self, dt):
        if self.run_epoch_counter < self.sh.cal.n_trials:
            self.beep()
            Clock.schedule_once(self.set_pause, self.sh.cal.pause_offset)
            Clock.schedule_once(self.set_cue, self.sh.cal.cue_offset)
            Clock.schedule_once(
                self.set_blank, self.sh.cal.cue_offset + self.sh.cal.cue_time)
        else:
            self.stop_run()

    def set_pause(self, dt):
        # self.carousel.index = 0
        self.sm.MarkEvents(0)

    def set_cue(self, dt):

        if self.stim_list[self.epoch_counter] == 1:
            # self.carousel.index = 1
            self.sm.MarkEvents(1)
            anim_left = threading.Thread(target=self.animate_bar_left)
            anim_left.start()

        elif self.stim_list[self.epoch_counter] == 2:
            # self.carousel.index = 2
            self.sm.MarkEvents(2)
            anim_right = threading.Thread(target=self.animate_bar_right)
            anim_right.start()

        self.epoch_counter += 1
        self.run_epoch_counter += 1

    def set_blank(self, dt):
        self.carousel.index = 3

    def beep(self):
        os.system(
            'play --no-show-progress --null --channels 1 \
            synth %s sine %f &' % (0.3, 500))

    def save_data(self):

        print('Saving data')
        self.sm.SaveData(self.sh.cal.data_cal_path)
        self.sm.SaveEvents(self.sh.cal.events_cal_path)

    def generate_stim_list(self):
        nt = self.sh.cal.n_trials * self.sh.cal.n_runs
        ones = np.ones(nt / 2)
        twos = 2 * np.ones(nt / 2)

        slist = np.concatenate([ones, twos])

        random.shuffle(slist)

        self.stim_list = slist.astype(int)

    def set_bar_default(self):

        self.inst_prob_left = 50
        self.inst_prob_right = 50
        self.accum_color_left = [1, 0, 0, 1]
        self.accum_color_right = [0, 0, 1, 1]

    def animate_bar_left(self):
        ts = time.time()
        tf = 0
        while tf < self.sh.cal.cue_time and self.stream_flag:
            ratio = tf / self.sh.cal.cue_time
            self.inst_prob_left = 50 + ratio * 50
            # if self.inst_prob_left > 80:
            #     self.accum_color_left = [1, 1, 0, 1]
            # else:
            #     self.accum_color_left = [1, 0, 0, 1]
            self.inst_prob_right = 100 - self.inst_prob_left
            time.sleep(0.05)
            tf = (time.time() - ts)

        self.set_bar_default()

    def animate_bar_right(self):
        ts = time.time()
        tf = 0
        while tf < self.sh.cal.cue_time and self.stream_flag:
            ratio = tf / self.sh.cal.cue_time
            self.inst_prob_right = 50 + ratio * 50
            # if self.inst_prob_right > 80:
            #     self.accum_color_right = [1, 1, 0, 1]
            # else:
            #     self.accum_color_right = [0, 0, 1, 1]
            self.inst_prob_left = 100 - self.inst_prob_right
            time.sleep(0.05)
            tf = (time.time() - ts)

        self.set_bar_default()
