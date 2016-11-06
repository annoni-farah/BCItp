import numpy as np
import matplotlib.pyplot as plt

delt = 50.0E-3
ki = 1

# u = 1
U = 0
U_time = np.array([])
U_MAX = 100

u_time = np.array([])
u_time = np.append(u_time, 	np.ones(101))
u_time = np.append(u_time, 	np.zeros(100))
u_time = np.append(u_time, 	-np.ones(101))
u_time = np.append(u_time, 	np.zeros(100))


TSTART = 0.
TSTOP = u_time.shape[0] * delt
time = np.linspace(TSTART, TSTOP, (TSTOP - TSTART) / delt)

for u in u_time:
    U += u
    if abs(U) > U_MAX:
    	U = 0
    U_time = np.append(U_time, U)

plt.subplot(2,1,1)
plt.plot(time, U_time, 'k', linewidth=4.0)
plt.grid(True)
plt.axis([0, 20, -150, 150])
# plt.axis('equal')
plt.ylabel('U')
# plt.xlabel('Time (s)')
plt.grid(True)
# plt.legend(loc=0)

plt.subplot(2,1,2)
plt.plot(time, u_time, 'k', linewidth=4.0)
plt.grid(True)
plt.axis([0, 20, -1.2, 1.2])
# plt.axis('equal')
plt.ylabel('u')
plt.xlabel('Time (s)')
plt.grid(True)

plt.show()
