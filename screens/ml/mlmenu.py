############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty, \
                            ListProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


# KV file:
Builder.load_file('screens/ml/mlmenu.kv')

# Generic:

# Project's:
from standards import *
from approach import Approach
######################################################################


class MlMenu(Screen):

# layout
    def __init__ (self, session_header, **kwargs):
        super (MlMenu, self).__init__(**kwargs)
        self.sh = session_header

    def change_to_calsettings(self,*args):
        self.manager.current = 'PreCalSettings'
        self.manager.transition.direction = 'left'

    def change_to_bci(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def save_config(self):

        ids = self.ids

        self.sh.epoch_start = ids.epoch_start.value
        self.sh.epoch_end = ids.epoch_end.value
        self.sh.nei = ids.csp_nei.value
        self.sh.class_ids = map(int,ids.class_ids.value.split(' '))

        self.sh.saveToPkl()

    def get_ml_model(self,*args):

        self.save_config()

        pup = popupMl(self.sh)

        popup = Popup(title='Machine Learning Results', content=pup,
            size_hint=(None, None), size=(400, 200))

        popup.open()


class popupMl(BoxLayout):

    def __init__(self, session_header, **kwargs):
        super(popupMl, self).__init__(**kwargs)

        sh = session_header

        ap = Approach()

        ap.defineApproach(sh.sample_rate, sh.f_low, sh.f_high, sh.f_order, sh.nei,
            sh.class_ids, sh.epoch_start, sh.epoch_end)

        ap.setPathToCal(sh.data_cal_path, sh.events_cal_path)
        ap.setPathToVal(sh.data_val_path,sh.events_val_path)

        ap.setValidChannels(sh.channels)

        autoscore = ap.trainModel()
        autoscore = round(autoscore, 3)

        valscore = ap.validateModel()
        valscore = round(valscore, 3)

        ap.saveToPkl(PATH_TO_SESSION + sh.name)

        self.orientation = 'vertical'

        autoBox = BoxLayout()
        l1 = Label(text='Self Val Acc: %', font_size = FONT_SIZE)
        l2 = Label(text=str(autoscore), font_size = FONT_SIZE) 
        autoBox.add_widget(l1)
        autoBox.add_widget(l2)

        valBox = BoxLayout()
        l3 = Label(text='Val Acc: %', font_size = FONT_SIZE)
        l4 = Label(text=str(valscore), font_size = FONT_SIZE) 
        valBox.add_widget(l3)
        valBox.add_widget(l4)

        self.add_widget(autoBox)
        self.add_widget(valBox)