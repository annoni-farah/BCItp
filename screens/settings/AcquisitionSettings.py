############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty, \
                            ListProperty, BooleanProperty
from kivy.lang import Builder

# KV file:
Builder.load_file('screens/settings/acquisitionsettings.kv')

# Generic:

# Project's:
from SampleManager import *
from standards import *
from approach import Approach
######################################################################


from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

from utils import saveObjAsJson

from standards import *

from settings import *

class AcquisitionSettings(Screen):

    sman = ObjectProperty(None)
    mode_menu = ObjectProperty(None)


# layout
    def __init__ (self, session_header,**kwargs):
        super (AcquisitionSettings, self).__init__(**kwargs)
        self.sh = session_header

        self.daisy = False

    def change_to_bci(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def enable_openbci_config(self, checkbox, value):
        if value:
            self.box_text.add_widget(self.box_text_openbci)
            self.mode = 'openbci'
        else:
            self.box_text.remove_widget(self.box_text_openbci)

    def enable_simu_config(self, checkbox, value):
        if value:
            self.box_text.add_widget(self.box_text_simu)
            self.mode = 'simu'
        else:
            self.box_text.remove_widget(self.box_text_simu)

    def enable_playback_config(self, checkbox, value):
        if value:
            self.box_text.add_widget(self.box_text_playback)
            self.mode = 'playback'
        else:
            self.box_text.remove_widget(self.box_text_playback)

    def enable_daisy(self, checkbox, value):
        if value:
            self.daisy = True
        else:
            self.daisy = False

    def save_config(self,*args):

        simulator_ids = self.sman.simulator.ids
        openbci_ids = self.sman.openbci.ids

        self.sh.mode = self.sman.current
        self.sh.com_port = openbci_ids.com_port
        self.sh.ch_labels = openbci_ids.ch_labels
        self.sh.baud_rate = openbci_ids.baud_rate
        self.sh.path_to_file = simulator_ids.eeg_path
        self.sh.path_to_labels_file = simulator_ids.labels_path
        self.sh.sample_rate = simulator_ids.srate
        self.sh.daisy = openbci_ids.daisy

        if (self.sh.mode == 'openbci'):
            if (self.sh.daisy):
                self.sh.sample_rate = 125
            else:
                self.sh.sample_rate = 250

        self.sh.saveToPkl()
        self.label_msg.text = "Settings Saved!"

class Menu(GridLayout):
    pass

class SettingsScreens(ScreenManager):
    simulator = ObjectProperty(None)
    openbci = ObjectProperty(None)


class Simulator(Screen):
    eeg_path = StringProperty('')
    labels_path = StringProperty('')
    srate = NumericProperty(0)    


class OpenBCI(Screen):
    pass
