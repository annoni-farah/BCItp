import numpy as np
import scipy.io as sio
import sys


mat_data = sio.loadmat(sys.argv[1])

np.save(sys.argv[2], mat_data)