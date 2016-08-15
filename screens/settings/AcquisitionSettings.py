############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty, \
                            ListProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

# KV file:
Builder.load_file('screens/settings/acquisitionsettings.kv')

# Generic:

# Project's:
from SampleManager import *
from standards import *
from approach import Approach
######################################################################

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

    def save_config(self,*args):

        simulator_ids = self.sman.simulator.ids
        openbci_ids = self.sman.openbci.ids

        self.sh.mode = self.sman.current
        self.sh.com_port = openbci_ids.com_port.value
        self.sh.ch_labels = openbci_ids.ch_labels.value
        self.sh.baud_rate = openbci_ids.baud_rate.value
        self.sh.path_to_file = simulator_ids.eeg_path.value
        self.sh.path_to_labels_file = simulator_ids.labels_path.value
        self.sh.sample_rate = simulator_ids.srate.value
        self.sh.daisy = openbci_ids.daisy.value

        if (self.sh.mode == 'openbci'):
            if (self.sh.daisy):
                self.sh.sample_rate = 125
            else:
                self.sh.sample_rate = 250

        self.sh.saveToPkl()

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
