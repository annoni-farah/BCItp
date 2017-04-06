import unittest

from bcitp.core.data_handler import DataHandler


class DataHandlerTestCase(unittest.TestCase):

    def setUp(self):
        # import class and prepare everything here.
        self.dh = DataHandler(p='/dev/ttyUSB0',
                              buf_len=500,
                              daisy=True,
                              mode='simu',
                              playback_path=None,
                              dummy=True)

    def test_YYY(self):
        # place your test case here
        a = 1
        self.assertEqual(a, 1)
