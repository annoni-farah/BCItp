import numpy as np
import matplotlib.pyplot as plt
import math

CHECKPOINTx = [0, 0, -20, -20, 20]
CHECKPOINTy = [-20, 0, 0, 20, 20]

r_sum = None
N = [1, 2, 3, 4, 5, 8, 9, 10]
runtime = []
for i in N:
    RESULTS_PATH = '/home/rafael/codes/bci_training_platform/data/' + \
        'session/A4_comp_drone/drone_runs_official/game_data_run' + \
        str(i) + '.npy'

    d = np.load(RESULTS_PATH)
    r = d[0]
    r = r[1:]  # remove first point

    plt.plot(r[:, 0], r[:, 1])

    if r_sum is None:
        r_sum = np.zeros([554, 2])

    r_sum = np.sum([r_sum, r[:r_sum.shape[0], :]], axis=0)

    t = d[1]

    runtime.append(t)

r_tot = r_sum / (len(N))
time_avg = sum(runtime) / len(runtime)


# PLOT PATH
plt.plot(r_tot[:, 0], r_tot[:, 1], 'k', linewidth=4.0, label='Mean')
plt.plot(CHECKPOINTx, CHECKPOINTy, 'ro')
plt.axis([-60, 60, -60, 60])
plt.ylabel('Pos Y (m)')
plt.xlabel('Pos X (m)')
plt.grid(True)
plt.legend()

plt.show()

# PLOT RUNTIME
my_xticks = [str(i) for i in N]
x = range(len(N))
tavg = np.empty([len(N)])
tavg[:] = time_avg
plt.xticks(x, my_xticks)
plt.bar(x, runtime, align='center', alpha=0.5)
plt.plot(x, tavg, 'k', linewidth=4.0, label='Mean')
plt.xlabel('Run Number')
plt.ylabel('Time (s)')
plt.legend()
plt.grid(True)
plt.show()
