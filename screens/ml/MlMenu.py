from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.popup import Popup

from standards import *

from utils import saveObjAsJson

from CSPLDAapproach import apply_ml

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

        button_dinfo = Button(text="Data Info", size = BUTTON_SIZE)
        button_dinfo.bind(on_press= self.show_data_info)

        button_save = Button(text="Save Config", size = BUTTON_SIZE)
        button_save.bind(on_press= self.save_config)

        button_train = Button(text="Train and evaluate Model", size = BUTTON_SIZE)
        button_train.bind(on_press= self.get_ml_model)

        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_save)
        box_bottom.add_widget(button_dinfo)
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

        self.sh.ml_epoch_start = self.epoch_start.text
        self.sh.ml_epoch_end = self.epoch_end.text
        self.sh.ml_pp_method = self.pp_method.text
        self.sh.ml_pp_nei = self.pp_nei.text
        self.sh.ml_class_ids = self.class_ids.text

        saveObjAsJson(self.sh, PATH_TO_SESSION + self.sh.name + '/' + 'session_info.txt')
        self.label_msg.text = "Settings Saved!"

    def get_ml_model(self,*args):

        pup = popupMl(self.sh)

        popup = Popup(title='Machine Learning Results', content=pup,
            size_hint=(None, None), size=(400, 200))

        popup.open()
        
    def show_data_info(self,*args):

        pup = popupDataInfo(self.sh)

        popup = Popup(title='Data Info', content=pup,
            size_hint=(None, None), size=(400, 400))

        popup.open()



class popupMl(BoxLayout):

    def __init__(self, session_header, **kwargs):
        super(popupMl, self).__init__(**kwargs)

        sh = session_header

        epoch_start, epoch_end, \
            method, neibourghs, ids = sh.getMachineLearningConfig()

        buf_len, f_low, f_high, \
            f_order, channels, notch = sh.getDataProcessingConfig()

        mode, com_port, baud_rate, \
            ch_labels, path_to_file, fs, daisy = sh.getAcquisitionConfig()

        results = apply_ml(sh.data_cal_path, sh.events_cal_path, sh.data_val_path,
            sh.events_val_path, fs,  f_low, f_high, f_order, neibourghs,
            ids, epoch_start, epoch_end)

        self.orientation = 'horizontal'

        l1 = Label(text='Acc: %', font_size = FONT_SIZE)
        l2 = Label(text=str(results), font_size = FONT_SIZE) 

        self.add_widget(l1)
        self.add_widget(l2)

class popupDataInfo(BoxLayout):

    def __init__(self, session_header, **kwargs):
        super(popupDataInfo, self).__init__(**kwargs)

        sh = session_header

        session_name, date, desc = sh.getSessionConfig()

        epoch_start, epoch_end, \
            method, neibourghs, ids = sh.getMachineLearningConfig()

        buf_len, f_low, f_high, \
            f_order, channels, notch = sh.getDataProcessingConfig()

        mode, com_port, baud_rate, \
            ch_labels, path_to_file, fs, daisy = sh.getAcquisitionConfig()

        self.orientation = 'vertical'

        b_name = BoxLayout() 
        l1 = Label(text='Session Name', font_size = FONT_SIZE)
        l2 = Label(text=session_name, font_size = FONT_SIZE)
        b_name.add_widget(l1)
        b_name.add_widget(l2)

        b_chlabels = BoxLayout() 
        l1 = Label(text='Channel Labels', font_size = FONT_SIZE)
        l2 = Label(text=ch_labels, font_size = FONT_SIZE)
        b_chlabels.add_widget(l1)
        b_chlabels.add_widget(l2)

        self.add_widget(b_name)
        self.add_widget(b_chlabels)