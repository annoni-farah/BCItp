from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import os

class StartScreen(Screen):
# layout
    def __init__ (self,**kwargs):
        super (StartScreen, self).__init__(**kwargs)

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.5,padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=20)

        button_ui_settings = Button(text="UIX Settings")
        button_ui_settings.bind(on_press= self.change_to_ui_settings)

        button_next = Button(text="BCI Menu")
        button_next.bind(on_press= self.change_to_bci)

        button_save = Button(text="Save")
        button_save.bind(on_press= self.save_username)

        self.username = TextInput(size_hint=(1, 0.8), font_size= 20,
            hint_text='Username', multiline=False)

        box1.add_widget(self.label_msg)
        box1.add_widget(self.username)
        box1.add_widget(button_save)
        box1.add_widget(button_ui_settings)
        box1.add_widget(button_next)
        self.add_widget(box1)

    def change_to_ui_settings(self,*args):
        self.manager.current = 'UISettings'
        self.manager.transition.direction = 'left'

    def change_to_bci(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'left'

    def save_username(self,*args):
        if os.path.exists("data/" + self.username.text):
            self.label_msg.text = "Username " + self.username.text + " already exists. Data will be replaced!"
        else:
            self.label_msg.text = "UserName Saved as: " + self.username.text
            os.makedirs("data/" + self.username.text)