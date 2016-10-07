import numpy as np
import sys


txt_data = np.loadtxt(sys.argv[1])
np.save(sys.argv[2], txt_data)