# -*- coding: utf-8 -*-
"""
Simulates data being sent from OpenBCI V3 board. Useful for applications testing. The ouput data is always 0 as if the daisy module was not connected.



"""
import struct
import numpy as np
import time
import timeit

SAMPLE_RATE = 250.0  # Hz

class OpenBCIBoard(object):
  """

  Handle a connection to an OpenBCI board.

  Args:
    port: The port to connect to.
    baud: The baud of the serial connection.
    daisy: Enable or disable daisy module and 16 chans readings
  """

  def __init__(self, port=None, baud=115200, data = [], filter_data=True,
    scaled_output=True, daisy=False, log=True, timeout=None):

    print("Connecting to V3 simulator")
    #wait for device to be ready

    self.streaming = False
    self.scaling_output = scaled_output

    self.t = 0

    self.playback_data = data
    self.playback_data_shape = data.shape

    self.daisy = daisy

    self.sample_rate = self.getSampleRate()

  def getSampleRate(self):
    if self.daisy:
      return SAMPLE_RATE/2.0
    else:
      return SAMPLE_RATE

  def start_streaming(self, callback, lapse=-1):
    """
    Start handling streaming data from the board. Call a provided callback
    for every single sample that is processed (every two samples with daisy module).

    Args:
      callback: A callback function -- or a list of functions -- that will receive a single argument of the
          OpenBCISample object captured.
    """
    if not self.streaming:
      self.streaming = True

    start_time = timeit.default_timer()

    # Enclose callback funtion in a list if it comes alone
    if not isinstance(callback, list):
      callback = [callback]

    sample_counter = 0
    counter_max = self.playback_data_shape[0]
    
    while self.streaming:
      
      st = time.time()
      # read current sample
      packet_id = 0

      channel_data = self.playback_data[sample_counter,:].tolist()

      sample = OpenBCISample(packet_id, channel_data, [])
      # if a daisy module is attached, wait to concatenate two samples (main board + daisy) before passing it to callback
      for call in callback:
        call(sample)
      
      if(lapse > 0 and timeit.default_timer() - start_time > lapse):
        self.stop();

      sample_counter += 1

      if sample_counter == counter_max:
        sample_counter=0

      while 1.0 / self.sample_rate > time.time() - st:
        pass
      # time.sleep(1.0 / SAMPLE_RATE)
  
  
  """

  Clean Up (atexit)

  """
  def stop(self):
    print("Stopping streaming...\nWait for buffer to flush...")
    self.streaming = False
    
    
  def disconnect(self):
      print("Closing Serial...")
       

  """

      SETTINGS AND HELPERS

  """
  def warn(self, text):
      
    print("Warning: %s" % text)


class OpenBCISample(object):
  """Object encapulsating a single sample from the OpenBCI board."""
  def __init__(self, packet_id, channel_data, aux_data):
    self.id = packet_id;
    self.channel_data = channel_data;
    self.aux_data = aux_data;
