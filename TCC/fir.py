import numpy as np
from scipy import signal as sg
from matplotlib import pyplot as plt

fs=250
n_order=250
f1_2=[8,20]
b = sg.firwin(n_order,f1_2,pass_zero=False,window='blackman',nyq=fs/2)
#w, h = sg.freqz(b)

"""fig = plt.figure()
plt.title('Digital filter frequency response')

ax1 = fig.add_subplot(111)

plt.plot((w*fs)/(2*np.pi), 20 * np.log10(abs(h)), 'b')
plt.ylabel('Amplitude [dB]', color='b')
plt.xlabel('Frequencia [Hz]')

ax2 = ax1.twinx()
angles = np.unwrap(np.angle(h))
plt.plot((w*fs)/(2*np.pi), angles, 'g')
plt.ylabel('Anglo (radianos)', color='g')
plt.grid()
plt.axis('tight')
plt.show()"""

f1=8
f2=20
t=np.arange(0,5,1/fs)
sinal = np.sin(2*np.pi*1*t)+np.sin(2*np.pi*10*t)+np.sin(2*np.pi*3*t)
#plt.plot(t,sinal)

saida=sg.convolve(sinal,b,mode='full')
plt.plot(saida)
plt.show()
	
