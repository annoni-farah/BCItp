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

  def __init__(self, port=None, baud=115200, filter_data=True,
    scaled_output=True, daisy=False, log=True, timeout=None):

    print("Connecting to V3 simulator")
    #wait for device to be ready
    # time.sleep(1)

    self.streaming = False
    self.scaling_output = scaled_output

    self.t = 0

  def getSampleRate(self):
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
    
    while self.streaming:
      
      time.sleep(1. / SAMPLE_RATE)
      # read current sample
      packet_id = 0
      channel_data = np.random.rand(8,1).tolist()

      f = [5, 20, 30, 60, 80]
      A = [0, 0, 0, 5, 0]

      signal =A[0]*np.sin(2 * np.pi * f[0] * self.t / SAMPLE_RATE) + \
              A[1]*np.sin(2 * np.pi * f[1] * self.t / SAMPLE_RATE) + \
              A[2]*np.sin(2 * np.pi * f[2] * self.t / SAMPLE_RATE) + \
              A[3]*np.sin(2 * np.pi * f[3] * self.t / SAMPLE_RATE) + \
              A[4]*np.sin(2 * np.pi * f[4] * self.t / SAMPLE_RATE) 

      channel_data = [signal, 2*signal, signal, signal, signal, signal, signal, signal]

      sample = OpenBCISample(packet_id, channel_data, [])
      # if a daisy module is attached, wait to concatenate two samples (main board + daisy) before passing it to callback
      for call in callback:
        call(sample)
      
      if(lapse > 0 and timeit.default_timer() - start_time > lapse):
        self.stop();

      self.t += 1
  
  
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
