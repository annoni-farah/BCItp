import numpy as np
import matplotlib.pyplot as plt

RESULTS_PATH = '/home/rafael/codes/bci_training_platform/data/session/A1_comp/game_results_hit2.npy'

CHECKPOINTx = [0, -20, -20, 20]
CHECKPOINTy = [0, 0, 20, 20]

r = np.load(RESULTS_PATH)
r = r[1:]  # remove first point

plt.plot(r[:, 0], r[:, 1])
plt.plot(CHECKPOINTx, CHECKPOINTy, 'ro')
plt.axis([-30, 30, -30, 30])
plt.grid(True)

plt.show()
