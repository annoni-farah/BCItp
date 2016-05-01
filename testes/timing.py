import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen


class MyApp(App):

    def build(self):
            bci_screen = BCIMenu(name='BCIMenu')

            sm.add_widget(game_screen)

            sm.current = 'start'
            return sm



# run app
if __name__ == "__main__":
    MyApp().run()
 # join all items in a list into 1 big string