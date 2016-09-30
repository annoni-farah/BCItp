# DEPENDENCIES-------------------------
# Generic:

# Project's:

# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

# KV file:
Builder.load_file('screens/settings/acquisitionsettings.kv')


######################################################################

class AcquisitionSettings(Screen):

    sman = ObjectProperty(None)
    mode_menu = ObjectProperty(None)

# layout
    def __init__(self, session_header, **kwargs):
        super(AcquisitionSettings, self).__init__(**kwargs)
        self.sh = session_header

        self.daisy = False

    def change_to_bci(self, *args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def save_config(self, *args):

        simulator_ids = self.sman.simulator.ids
        openbci_ids = self.sman.openbci.ids

        self.sh.acq.mode = self.sman.current
        self.sh.acq.com_port = openbci_ids.com_port.value
        self.sh.acq.ch_labels = openbci_ids.ch_labels.value
        self.sh.acq.path_to_file = simulator_ids.eeg_path.value
        self.sh.acq.path_to_labels_file = simulator_ids.labels_path.value
        self.sh.acq.dummy = simulator_ids.dummy_data.value

        if self.sh.acq.dummy:
            self.sh.acq.daisy = True

        else:
            self.sh.acq.daisy = openbci_ids.daisy.value

        if self.sh.acq.mode == 'openbci':
            if self.sh.acq.daisy:
                self.sh.acq.sample_rate = 125
            else:
                self.sh.acq.sample_rate = 250
        else:
            self.sh.acq.sample_rate = simulator_ids.srate.value

        self.sh.acq.flag = True
        self.sh.saveToPkl()

    def update_settings(self):

        simulator_ids = self.sman.simulator.ids
        openbci_ids = self.sman.openbci.ids

        self.sman.current = self.sh.acq.mode
        openbci_ids.com_port.value = self.sh.acq.com_port
        openbci_ids.ch_labels.value = self.sh.acq.ch_labels
        simulator_ids.eeg_path.value = self.sh.acq.path_to_file
        simulator_ids.labels_path.value = self.sh.acq.path_to_labels_file
        simulator_ids.srate.value = self.sh.acq.sample_rate
        simulator_ids.dummy_data.value = self.sh.acq.dummy
        openbci_ids.daisy.value = self.sh.acq.daisy


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
