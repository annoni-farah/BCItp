from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from standards import *

class ErrorPopup(BoxLayout):

    def __init__(self, **kwargs):
        super(popupDataInfo, self).__init__(**kwargs)

        l1 = Label(text='Error Data', font_size = FONT_SIZE)
        self.add_widget(l1)