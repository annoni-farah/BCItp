from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class UISettingsScreen(Screen):
# layout
    def __init__ (self, session_header, **kwargs):
        super (UISettingsScreen, self).__init__(**kwargs)
        self.sh = session_header

        box1 = BoxLayout(padding=10, orientation='vertical')

        button1 = Button(text="Back")
        button1.bind(on_press= self.change_to_start)

        button2 = Button(text="Print Session Name")
        button2.bind(on_press= self.display_name)

        box1.add_widget(button2)
        box1.add_widget(button1)

        self.add_widget(box1)

    def change_to_start(self,*args):
        self.manager.current = 'start'
        self.manager.transition.direction = 'right'

    def display_name(self,*args):
        print self.sh.name