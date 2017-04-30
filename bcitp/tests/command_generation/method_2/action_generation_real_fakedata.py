import numpy as np
import matplotlib.pyplot as plt

# =================================
# =========== VARIABLES ===========

delt = 50.0E-3
ki = 1

U1 = 0
U2 = 0

U1_time = np.array([])
U2_time = np.array([])

U1_MAX = 100
U2_MAX = 100

m_acc = 0.9

c_time = np.array([])
# c_time = np.append(c_time,  np.zeros(100))
# c_time = np.append(c_time,  -np.ones(200))
# c_time = np.append(c_time,  np.ones(200))

c_time = np.random.choice([-1, 1], [400], p=[m_acc, 1 - m_acc])


# c_time = np.append(c_time,  np.zeros(100))


TSTART = 0.
TSTOP = c_time.shape[0] * delt
time = np.linspace(TSTART, TSTOP, (TSTOP - TSTART) / delt)

# =================================
# =========== ALGORITHM ===========

for c in c_time:
    u1 = 0
    u2 = 0
    if c < 0:
        u1 = 1
    else:
        u2 = 1

    U1 += u1
    U2 += u2
    # if abs(U) > U_MAX:
    # U = 0
    U1_time = np.append(U1_time, U1)
    U2_time = np.append(U2_time, U2)


U1_model = m_acc * delt * c_time.shape[0] * time
U2_model = (1 - m_acc) * delt * c_time.shape[0] * time

# ================================
# =========== PLOTTING ===========
plt.subplot(2, 1, 1)
plt.plot(time, U1_time, 'k', linewidth=4.0, label='U1')
plt.plot(time, U2_time, 'k', color='0.50', linewidth=4.0, label='U2')
plt.plot(time, U1_model, 'b--', linewidth=2.0, label='U1 Model')
plt.plot(time, U2_model, 'r--', linewidth=2.0, label='U2 Model')
plt.grid(True)
plt.axis([0, 20, -20, 500])
# plt.axis('equal')
plt.ylabel('U')
# plt.xlabel('Time (s)')
plt.grid(True)
plt.legend(loc=0)

plt.subplot(2, 1, 2)
plt.plot(time, c_time, 'k', linewidth=2.0, label='Accuracy = 0.9')
plt.axis([0, 20, -1.2, 2])
# plt.axis('equal')
plt.ylabel('c')
plt.xlabel('Time (s)')
plt.grid(True)
plt.legend(loc=0)


plt.show()
