# -*- coding: utf-8 -*-
"""
Simulates data being sent from OpenBCI V3 board. Useful for applications testing. The ouput data is always 0 as if the daisy module was not connected.



"""
import struct
import numpy as np
import time
import timeit
import atexit
import logging
import threading
import sys
import pdb

SAMPLE_RATE = 250.0  # Hz
START_BYTE = 0xA0  # start of data packet
END_BYTE = 0xC0  # end of data packet
ADS1299_Vref = 4.5  #reference voltage for ADC in ADS1299.  set by its hardware
ADS1299_gain = 24.0  #assumed gain setting for ADS1299.  set by its Arduino code
scale_fac_uVolts_per_count = ADS1299_Vref/float((pow(2,23)-1))/ADS1299_gain*1000000.
scale_fac_accel_G_per_count = 0.002 /(pow(2,4)) #assume set to +/4G, so 2 mG 
'''
#Commands for in SDK http://docs.openbci.com/software/01-Open BCI_SDK:

command_stop = "s";
command_startText = "x";
command_startBinary = "b";
command_startBinary_wAux = "n";
command_startBinary_4chan = "v";
command_activateFilters = "F";
command_deactivateFilters = "g";
command_deactivate_channel = {"1", "2", "3", "4", "5", "6", "7", "8"};
command_activate_channel = {"q", "w", "e", "r", "t", "y", "u", "i"};
command_activate_leadoffP_channel = {"!", "@", "#", "$", "%", "^", "&", "*"};  //shift + 1-8
command_deactivate_leadoffP_channel = {"Q", "W", "E", "R", "T", "Y", "U", "I"};   //letters (plus shift) right below 1-8
command_activate_leadoffN_channel = {"A", "S", "D", "F", "G", "H", "J", "K"}; //letters (plus shift) below the letters below 1-8
command_deactivate_leadoffN_channel = {"Z", "X", "C", "V", "B", "N", "M", "<"};   //letters (plus shift) below the letters below the letters below 1-8
command_biasAuto = "`";
command_biasFixed = "~";
'''

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
#    self.ser = serial.Serial(port= port, baudrate = baud, timeout=timeout)

    time.sleep(2)


    #wait for device to be ready
    time.sleep(1)

    self.streaming = False
    self.filtering_data = filter_data
    self.scaling_output = scaled_output
    self.eeg_channels_per_sample = 8 # number of EEG channels per sample *from the board*
    self.aux_channels_per_sample = 3 # number of AUX channels per sample *from the board*
    self.read_state = 0
    self.daisy = daisy
    self.last_odd_sample = OpenBCISample(-1, [], []) # used for daisy
    self.log_packet_count = 0
    self.attempt_reconnect = False
    self.last_reconnect = 0
    self.reconnect_freq = 5
    self.packets_dropped = 0

    #Disconnects from board when terminated
    atexit.register(self.disconnect)
  
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
      channel_data = [0,0,0,0,0,0,0,0]  
      sample = OpenBCISample(packet_id, channel_data, [])
      # if a daisy module is attached, wait to concatenate two samples (main board + daisy) before passing it to callback
      for call in callback:
        call(sample)
      
      if(lapse > 0 and timeit.default_timer() - start_time > lapse):
        self.stop();
  
  
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
 

  def set_channel(self, channel, toggle_position):
    #Commands to set toggle to on position
    if toggle_position == 1:
      if channel is 1:
        self.ser.write(b'!')
      if channel is 2:
        self.ser.write(b'@')
      if channel is 3:
        self.ser.write(b'#')
      if channel is 4:
        self.ser.write(b'$')
      if channel is 5:
        self.ser.write(b'%')
      if channel is 6:
        self.ser.write(b'^')
      if channel is 7:
        self.ser.write(b'&')
      if channel is 8:
        self.ser.write(b'*')
      if channel is 9 and self.daisy:
        self.ser.write(b'Q')
      if channel is 10 and self.daisy:
        self.ser.write(b'W')
      if channel is 11 and self.daisy:
        self.ser.write(b'E')
      if channel is 12 and self.daisy:
        self.ser.write(b'R')
      if channel is 13 and self.daisy:
        self.ser.write(b'T')
      if channel is 14 and self.daisy:
        self.ser.write(b'Y')
      if channel is 15 and self.daisy:
        self.ser.write(b'U')
      if channel is 16 and self.daisy:
        self.ser.write(b'I')
    #Commands to set toggle to off position
    elif toggle_position == 0:
      if channel is 1:
        self.ser.write(b'1')
      if channel is 2:
        self.ser.write(b'2')
      if channel is 3:
        self.ser.write(b'3')
      if channel is 4:
        self.ser.write(b'4')
      if channel is 5:
        self.ser.write(b'5')
      if channel is 6:
        self.ser.write(b'6')
      if channel is 7:
        self.ser.write(b'7')
      if channel is 8:
        self.ser.write(b'8')
      if channel is 9 and self.daisy:
        self.ser.write(b'q')
      if channel is 10 and self.daisy:
        self.ser.write(b'w')
      if channel is 11 and self.daisy:
        self.ser.write(b'e')
      if channel is 12 and self.daisy:
        self.ser.write(b'r')
      if channel is 13 and self.daisy:
        self.ser.write(b't')
      if channel is 14 and self.daisy:
        self.ser.write(b'y')
      if channel is 15 and self.daisy:
        self.ser.write(b'u')
      if channel is 16 and self.daisy:
        self.ser.write(b'i')


class OpenBCISample(object):
  """Object encapulsating a single sample from the OpenBCI board."""
  def __init__(self, packet_id, channel_data, aux_data):
    self.id = packet_id;
    self.channel_data = channel_data;
    self.aux_data = aux_data;
