import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.bar import Bar

import collections

from math import sin

import numpy as np

class case(FloatLayout):

    def __init__(self, **kwargs):
        super(case, self).__init__(**kwargs)
        box = FloatLayout()

        b = Bar(orientation = 'bt', color=[0.07, 0.08, 0.4, 1])

        b.value = 50

        box.add_widget(b)

        self.add_widget(box)



class MyApp(App):

    def build(self):
    	return case()


# run app
if __name__ == "__main__":

    MyApp().run()
 # join all items in a list into 1 big string