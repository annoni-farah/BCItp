# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:27:59 2016

@author: rafael
"""
        
#slots_center = ([[100,60], [300,60], [500,60], [700,60], [900,60],
#        [100,180], [300,180], [500,180], [700,180], [900,180],
#        [100,300], [300,300], [500,300], [700,300], [900,300],
#        [100,420], [300,420], [500,420], [700,420], [900,420],
#        [100,540], [300,540], [500,540], [700,540], [900,540]])
        
import numpy as np


slots_X = [100, 300, 500, 700, 900]
slots_X[:] = [x - 55 for x in slots_X]

slots_Y = [60, 180, 300, 420, 540]
slots_Y[:] = [x - 20 for x in slots_Y]

slots = np.array([[slots_X[0], slots_Y[0]],
       [slots_X[1], slots_Y[0]],
       [slots_X[2], slots_Y[0]],
       [slots_X[3], slots_Y[0]],
       [slots_X[4], slots_Y[0]],
       [slots_X[0], slots_Y[1]],
       [slots_X[1], slots_Y[1]],
       [slots_X[2], slots_Y[1]],
       [slots_X[3], slots_Y[1]],
       [slots_X[4], slots_Y[1]],
       [slots_X[0], slots_Y[2]],
       [slots_X[1], slots_Y[2]],
       [slots_X[2], slots_Y[2]],
       [slots_X[3], slots_Y[2]],
       [slots_X[4], slots_Y[2]],
       [slots_X[0], slots_Y[3]],
       [slots_X[1], slots_Y[3]],
       [slots_X[2], slots_Y[3]],
       [slots_X[3], slots_Y[3]],
       [slots_X[4], slots_Y[3]],
       [slots_X[1], slots_Y[4]],
       [slots_X[2], slots_Y[4]],
       [slots_X[3], slots_Y[4]],
       [slots_X[4], slots_Y[4]]])

slots_max = np.copy(slots)

slots_max[:,0] = np.add(slots_max[:,0], 30)
slots_max[:,1] = np.add(slots_max[:,1], 55)