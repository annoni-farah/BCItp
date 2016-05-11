import numpy as np
import matplotlib.pyplot as plt

from DataProcessing import DataProcessing

import scipy.signal as sp


f_low = 25
f_high = 35
f_order = 7
fs = 250

dp = DataProcessing(1,30,250,11)

dp.DesignFilter('fir')

din = np.loadtxt('data_cal.txt')
t = np.arange(1000)
# din = np.sin(2 * np.pi * 25 * t / fs)


nyq = 0.5 * fs
low = f_low / nyq
high = f_high / nyq
b, a = sp.butter(f_order, [low, high], btype='band')

ch1 = din.T[0]

dout = sp.lfilter(b, a, ch1)

# dout = dp.ApplyFilter(din)

# print dout
plt.plot(dout)
plt.show()

plt.specgram(ch1, 1024, fs)
plt.show()

plt.specgram(dout, 1024, fs)
plt.show()


