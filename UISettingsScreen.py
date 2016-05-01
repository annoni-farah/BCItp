from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class UISettingsScreen(Screen):
# layout
    def __init__ (self,**kwargs):
        super (UISettingsScreen, self).__init__(**kwargs)

        box1 = BoxLayout(padding=10, orientation='vertical')
        button1 = Button(text="Back")
        button1.bind(on_press= self.change_to_start)
        box1.add_widget(button1)
        self.txt1 = TextInput(text='', multiline=False)
        box1.add_widget(self.txt1)
        self.add_widget(box1)

    def change_to_start(self,*args):
        self.manager.current = 'start'
        self.manager.transition.direction = 'right'