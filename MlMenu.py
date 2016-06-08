from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.popup import Popup

from standards import *

class MlMenu(Screen):
# layout
    def __init__ (self,**kwargs):
        super (MlMenu, self).__init__(**kwargs)

        boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label_msg = Label(text="", font_size=FONT_SIZE)
        ## BOTTOM PART (BUTTONS)

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, spacing=10, orientation='vertical')

        button_back = Button(text="Back", size_hint_x=1, size_hint_y=0.5)
        button_back.bind(on_press= self.change_to_cal)

        button_dinfo = Button(text="Data Info", size_hint_x=1, size_hint_y=0.5)
        button_dinfo.bind(on_press= self.show_data_info)

        button_train = Button(text="Train and evaluate Model", size_hint_x=1, size_hint_y=0.5)
        button_train.bind(on_press= self.get_ml_model)

        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_dinfo)
        box_bottom.add_widget(button_train)
        box_bottom.add_widget(button_back)

        boxg.add_widget(box_bottom)

        ## TOP PART

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.7,padding=10, spacing=10, orientation='vertical')

        # EPOCHS CONFIG
        box_epochs = BoxLayout(size_hint_x=1, size_hint_y=0.15,padding=10, spacing=10, orientation='horizontal')
        label_start = Label(text = 'Epoch Start', font_size=FONT_SIZE)
        self.epoch_start = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='2', multiline=False)
        label_end = Label(text = 'Epoch End', font_size=FONT_SIZE)
        self.epoch_end = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='4', multiline=False)

        box_epochs.add_widget(label_start)
        box_epochs.add_widget(self.epoch_start)
        box_epochs.add_widget(label_end)
        box_epochs.add_widget(self.epoch_end)
        
        box_top.add_widget(box_epochs)

        ## PRE PROCESSING
        box_pp = BoxLayout(size_hint_x=1, size_hint_y=0.15,padding=10, spacing=10, orientation='horizontal')
        label_pp_method = Label(text = 'Pre-Processing \n Method', font_size=FONT_SIZE)
        self.pp_method = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='CSP', multiline=False)

        label_pp_nei = Label(text = 'Neighbours pairs', font_size=FONT_SIZE)
        self.pp_nei = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='3', multiline=False)


        box_pp.add_widget(label_pp_method)
        box_pp.add_widget(self.pp_method)
        box_pp.add_widget(label_pp_nei)
        box_pp.add_widget(self.pp_nei)

        ## PRE PROCESSING
        box_clf = BoxLayout(size_hint_x=1, size_hint_y=0.15,padding=10, spacing=10, orientation='horizontal')
        label_clf_method = Label(text = 'Classifier Method', font_size=FONT_SIZE)
        self.clf_method = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='LDA', multiline=False)

        box_clf.add_widget(label_clf_method)
        box_clf.add_widget(self.clf_method)
        
        box_top.add_widget(box_pp)
        box_top.add_widget(box_clf)

        boxg.add_widget(box_top, 2)

        ##


        self.add_widget(boxg)

    def change_to_calsettings(self,*args):
        self.manager.current = 'PreCalSettings'
        self.manager.transition.direction = 'left'

    def change_to_cal(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def show_data_info(self,*args):
        box = BoxLayout()
        l1 = Label(text='Hello world')
        l2 = Label(text='Hello world') 

        box.add_widget(l1)
        box.add_widget(l2)

        popup = Popup(title='Test popup', content=box,
            size_hint=(None, None), size=(400, 400))

        popup.open()
        
    def get_ml_model(self,*args):
        box = BoxLayout()
        l1 = Label(text='Model Results')
        l2 = Label(text='Acc: %') 

        box.add_widget(l1)
        box.add_widget(l2)

        popup = Popup(title='Test popup', content=box,
            size_hint=(None, None), size=(400, 400))

        popup.open()