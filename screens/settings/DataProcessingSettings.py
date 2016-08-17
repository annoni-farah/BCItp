############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty, \
                            ListProperty, BooleanProperty
from kivy.lang import Builder

# KV file:
Builder.load_file('screens/settings/dataprocessingsettings.kv')

# Generic:

# Project's:
from SampleManager import *
from standards import *
from approach import Approach
######################################################################


class DataProcessingSettings(Screen):

# layout
    def __init__ (self, session_header,**kwargs):
        super (DataProcessingSettings, self).__init__(**kwargs)
        self.sh = session_header

    def change_to_bci(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def save_config(self,*args):

        ids = self.ids

        self.sh.buf_len = ids.buf_len.value
        self.sh.f_low = ids.f_low.value
        self.sh.f_high = ids.f_high.value
        self.sh.f_order = ids.f_order.value

        if ':' in ids.channels.value:
            limits=map(int,ids.channels.value.split(':'))
            ch_idx = range(limits[0],limits[1])
        else:
            ch_idx = map(int,ids.channels.value.split(' '))

        self.sh.channels = ch_idx

        self.sh.saveToPkl()
        self.msg = "Settings Saved!"

    def update_settings(self):

        ids = self.ids

        ids.buf_len.value= self.sh.buf_len
        ids.f_low.value = self.sh.f_low
        ids.f_high.value = self.sh.f_high
        ids.f_order.value = self.sh.f_order

        # not the best option but it works
        ids.channels.value = str(self.sh.channels).replace(',','').replace('[', '').replace(']', '')
