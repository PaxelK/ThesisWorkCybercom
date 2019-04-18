# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:42:20 2019

@author: axkar1
"""

from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt  

# create GEKKO model
m = GEKKO(remote=False)
# time points
n=501
m.time = np.linspace(0,10,n)
# constants

Eelec = 50*10^(-9)
Eamp = 100*10^(-12)
EDA = 5*10^(-9)
Egen = 1*10^(-5)
PRmax = 20000
const = 0.6

packet = 1
E = 1
# fishing rate
p = m.FV()
p.STATUS = 1
pr = m.MV(value=1,lb=0,ub=1)
pr.STATUS = 1
pr.DCOST = 0

nrj = m.Var(value=0.7)                  # Energy Amount
myObj = m.Var(value=0)
d = m.Var(value=70)                     # Distance to receiver
d2 = m.Intermediate(d**2)

# fish population balance
m.Equation(nrj.dt() == Egen - ((Eelec+EDA)*packet + pr*PRmax*(Eelec + Eamp * d2)))
m.Equation(d.dt() == -0.5)
m.Equation(myObj.dt() == (E-const/nrj)*pr*PRmax)

m.Connection(p,myObj,pos2='end')

m.Obj(-myObj)

#J = m.Var(value=0)                      # objective (profit)
#Jf = m.FV()                             # final objective
#Jf.STATUS = 1
#m.Connection(Jf,J,pos2='end')
#m.Equation(J.dt() == (E-const/nrj)*pr*PRmax)
#m.Obj(-Jf)                              # maximize profit by minimizing negative profit

m.options.IMODE = 6                     # optimal control
m.options.NODES = 3                     # collocation nodes
m.options.SOLVER = 3                    # solver (IPOPT)
m.solve(disp=False)                     # Solve
print('Optimal Profit: ' + str(Jf.value[0]))
plt.figure(1)                           # plot results
plt.subplot(2,1,1)
plt.plot(m.time,J.value,'r--',label='Bits Sent')
plt.plot(m.time,nrj.value,'b-',label='EC')
plt.legend()
plt.subplot(2,1,2)
plt.plot(m.time,pr.value,'k--',label='PR')
plt.xlabel('Time (yr)')
plt.legend()
plt.show()