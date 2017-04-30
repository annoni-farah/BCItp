import unittest
import os.path as op
import sys

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)

from handlers.event_handler import EventHandler


class EventHandlerTestCase(unittest.TestCase):

    def setUp(self):
        '''
          Create a datahandler object and initiate a simulation board with
          dummy data
        '''
        self.eh = EventHandler()

    def test_event_mark(self):
        '''
          Run the acquistion for 1 second and check if number of
          samples collected is correct
        '''

        self.eh.mark_events(10, 1)
        self.eh.mark_events(500, 1)
        self.eh.mark_events(1550, 2)
        self.eh.mark_events(2000, 1)

        elist = self.eh.event_list

        self.assertEqual(elist.shape[0], 4)
        self.assertEqual(elist.shape[1], 2)
        self.assertEqual(elist[-1][0], 2000)
        self.assertEqual(elist[-1][1], 1)
