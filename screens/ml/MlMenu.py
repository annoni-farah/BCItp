from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.popup import Popup

from standards import *

from utils import saveObjAsJson

from approach import Approach


class MlMenu(Screen):
# layout
    def __init__ (self, session_header, **kwargs):
        super (MlMenu, self).__init__(**kwargs)
        self.sh = session_header

        boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label_msg = Label(text="", font_size=FONT_SIZE)

        ## TOP PART

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.7,padding=10, spacing=10, orientation='vertical')

        # EPOCHS CONFIG
        box_epochs = BoxLayout(size_hint_x=1, size_hint_y=0.15,padding=10, spacing=10, orientation='horizontal')
        
        label_start = Label(text = 'Epoch Start', font_size=FONT_SIZE)
        self.epoch_start = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='2', multiline=False)
        box_epochs.add_widget(label_start)
        box_epochs.add_widget(self.epoch_start)


        label_end = Label(text = 'Epoch End', font_size=FONT_SIZE)
        self.epoch_end = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='4', multiline=False)
        box_epochs.add_widget(label_end)
        box_epochs.add_widget(self.epoch_end)
        
        box_top.add_widget(box_epochs)

        ## PRE PROCESSING
        box_pp = BoxLayout(size_hint_x=1, size_hint_y=0.15,padding=10, spacing=10, orientation='horizontal')
        
        label_pp_method = Label(text = 'Pre-Processing \n Method', font_size=FONT_SIZE)
        self.pp_method = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='CSP', multiline=False)
        box_pp.add_widget(label_pp_method)
        box_pp.add_widget(self.pp_method)

        label_pp_nei = Label(text = 'Neighbours pairs', font_size=FONT_SIZE)
        self.pp_nei = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='3', multiline=False)
        box_pp.add_widget(label_pp_nei)
        box_pp.add_widget(self.pp_nei)
        
        box_top.add_widget(box_pp)

        box_clf = BoxLayout(size_hint_x=1, size_hint_y=0.15,padding=10, spacing=10, orientation='horizontal')
        label_clf_method = Label(text = 'Classifier Method', font_size=FONT_SIZE)
        self.clf_method = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='LDA', multiline=False)

        box_clf.add_widget(label_clf_method)
        box_clf.add_widget(self.clf_method)

        box_cid = BoxLayout(size_hint_x=1, size_hint_y=0.15,padding=10, spacing=10, orientation='horizontal')
        label_cid_method = Label(text = 'Classes ID', font_size=FONT_SIZE)
        self.class_ids = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='1 2', multiline=False)

        box_cid.add_widget(label_cid_method)
        box_cid.add_widget(self.class_ids)
        
        box_top.add_widget(box_cid)

        boxg.add_widget(box_top, 2)

        ##

        ## BOTTOM PART (BUTTONS)

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='vertical')

        button_back = Button(text="Back", size = BUTTON_SIZE)
        button_back.bind(on_press= self.change_to_cal)

        button_save = Button(text="Save Config", size = BUTTON_SIZE)
        button_save.bind(on_press= self.save_config)

        button_train = Button(text="Train and evaluate Model", size = BUTTON_SIZE)
        button_train.bind(on_press= self.get_ml_model)

        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_save)
        box_bottom.add_widget(button_train)
        box_bottom.add_widget(button_back)

        boxg.add_widget(box_bottom)

        self.add_widget(boxg)

    def change_to_calsettings(self,*args):
        self.manager.current = 'PreCalSettings'
        self.manager.transition.direction = 'left'

    def change_to_cal(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def save_config(self,*args):

        self.sh.epoch_start = float(self.epoch_start.text)
        self.sh.epoch_end = float(self.epoch_end.text)
        self.sh.method = self.pp_method.text
        self.sh.nei = int(self.pp_nei.text)
        self.sh.class_ids = map(int,self.class_ids.text.split(' '))

        self.sh.saveToPkl()
        self.label_msg.text = "Settings Saved!"

    def get_ml_model(self,*args):

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
        ap.setPathToVal( sh.data_val_path,sh.events_val_path)

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