import unittest
import os.path as op
import sys
from time import sleep

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)

from handlers.data_handler import DataHandler


class DataHandlerTestCase(unittest.TestCase):

    def setUp(self):
        '''
          Create a datahandler object and initiate a simulation board with
          dummy data
        '''
        self.dh = DataHandler(port='/dev/ttyUSB0',
                              buffer_len=500,
                              daisy=True,
                              mode='simu',
                              playback_data_path=None,
                              dummy=True)

        self.dh.init_board()

    def test_run(self):
        '''
          Run the acquistion for 1 second and check if number of
          samples collected is correct
        '''

        self.dh.start()
        sleep(1)
        self.dh.stop_flag = True
        self.dh.join()

        sample_counter = self.dh.sample_counter
        self.assertEqual(abs(sample_counter - 125) < 10, True)
