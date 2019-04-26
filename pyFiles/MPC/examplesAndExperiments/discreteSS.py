# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:04:16 2019

@author: axkar1
"""

import numpy as np
from gekko import GEKKO

A = np.array([[0,0,0,0],
              [1,0,0,0],
              [0,1,0,0],
              [0,0,1,0]])

B = np.array([[1],
              [0],
              [0],
              [0]])

C = np.array([[0, 0, 0, 1]])

#%% Build GEKKO State Space model
m = GEKKO()
x,y,u = m.state_space(A,B,C,D=None,discrete=True)

# customize names
mv0 = u[0]
# CVs
cv0 = y[0]

m.time = np.linspace(0,120,9)
mv0.value = np.zeros(9)
mv0.value[3:9] = 1
m.options.imode = 4
m.options.nodes = 2

m.solve() # (GUI=True)

# also create a Python plot
import matplotlib.pyplot as plt

plt.subplot(2,1,1)
plt.plot(m.time,mv0.value,'r-',label=r'$u_0$ as MV')
plt.legend()
plt.subplot(2,1,2)
plt.plot(m.time,cv0.value,'b--',label=r'$y_0$')
plt.legend()
plt.show()