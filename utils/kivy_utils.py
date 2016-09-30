from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from standards import FONT_SIZE


class ErrorPopup(BoxLayout):

    def __init__(self, **kwargs):
        super(popupDataInfo, self).__init__(**kwargs)

        l1 = Label(text='Error Data', font_size=FONT_SIZE)
        self.add_widget(l1)
