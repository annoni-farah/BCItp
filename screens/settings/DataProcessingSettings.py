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

    buf_len = ObjectProperty(None)
    channels = ObjectProperty(None)
    f_high = ObjectProperty(None)
    f_low = ObjectProperty(None)
    f_order = ObjectProperty(None)

    msg = StringProperty('')

    notch = BooleanProperty(False)

# layout
    def __init__ (self, session_header,**kwargs):
        super (DataProcessingSettings, self).__init__(**kwargs)
        self.sh = session_header

    def change_to_cal(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def enable_notch_filt(self, checkbox, value):
        
        print 'val:', value
        if value:
            self.notch = True
        else:
            self.notch = False


    def save_config(self,*args):

        self.sh.buf_len = int(self.buf_len.text)
        self.sh.f_low = int(self.f_low.text)
        self.sh.f_high = int(self.f_high.text)
        self.sh.f_order = int(self.f_order.text)
        self.sh.channels = map(int, self.channels.text.split(" "))
        self.sh.notch = self.notch

        self.sh.saveToPkl()
        self.msg = "Settings Saved!"
