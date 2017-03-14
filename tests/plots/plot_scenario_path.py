import numpy as np
import matplotlib.pyplot as plt

# CHECKPOINTx = [0, 0, -20, -20, 20]
# CHECKPOINTy = [-20, 0, 0, 20, 20]

CHECKPOINTx = [0, 0, 20, 20, -20]
CHECKPOINTy = [-20, 0, 0, 20, 20]

# PLOT PATH
# plt.plot(r_tot[:, 0], r_tot[:, 1], 'k', linewidth=4.0, label='Mean')
plt.plot(CHECKPOINTx, CHECKPOINTy, 'k',linewidth=4.0)
plt.plot(CHECKPOINTx[0], CHECKPOINTy[0], 'go')
plt.plot(CHECKPOINTx[1:-1], CHECKPOINTy[1:-1], 'ro', linewidth=4.0)
plt.plot(CHECKPOINTx[-1], CHECKPOINTy[-1], 'bo', linewidth=4.0)
plt.axis([-25, 25, -25, 25])
# plt.axis('equal')
plt.ylabel('Pos Y (m)')
plt.xlabel('Pos X (m)')
plt.grid(True)
plt.legend(loc=0)
plt.show()
