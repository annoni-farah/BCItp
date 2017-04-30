import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.graph import Graph, LinePlot

import collections

from math import sin

import numpy as np

class case(FloatLayout):

    def __init__(self, **kwargs):
        super(case, self).__init__(**kwargs)
        box = FloatLayout()
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
            x_ticks_major=25, y_ticks_major=1,
            y_grid_label=True, x_grid_label=True, padding=5,
            x_grid=True, y_grid=True, xmin=-0, xmax=20, ymin=0, ymax=10)
        plot = LinePlot()
        # plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]

        # data = np.array([[0,0], [1,1],[2,2]])

        data = collections.deque(maxlen = 20)
        time = collections.deque(maxlen = 20)

        d = (0,1,2,3,4,5,6,7,8,9)
        t = (0,1,2,3,4,5,6,7,8,9)

        data.append(d)
        time.append(t)

        toplot = np.vstack((time,data)).T

        print toplot

        plot.points = tuple(map(tuple, toplot))

        graph.add_plot(plot)
        box.add_widget(graph)

        self.add_widget(box)



class MyApp(App):

    def build(self):
    	return case()


# run app
if __name__ == "__main__":

    MyApp().run()
 # join all items in a list into 1 big string