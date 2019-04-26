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
n=11
m.time = np.linspace(0,10,n)

# constants
Eelec = 50*10**-9
Eamp = 100*10**-12
EDA = 5*10**-9
Egen = 1*10**-5
PRmax = 20
pSize = 2000
const = 0.6

conChildren = 1
E = 1

# packet rate
pr = m.MV(value=1, integer = True,lb=1,ub=20)
pr.STATUS = 1
pr.DCOST = 0

#packets = m.CV(value=0)
# Energy Stored
nrj = m.Var(value=0.05, lb=0)                  # Energy Amount
d = m.Var(value=70, lb = 0)                     # Distance to receiver
d2 = m.Intermediate(d**2)


# fish population balance
m.Equation(d.dt() == 1.5)
m.Equation(nrj >= Egen - ((Eelec+EDA)*conChildren + pr*pSize*(Eelec + Eamp * d2)))
m.Equation(nrj.dt() == Egen - ((Eelec+EDA)*conChildren + pr*pSize*(Eelec + Eamp * d2)))


# objective (profit)
J = m.Var(value=0)
# final objective
Jf = m.FV()
Jf.STATUS = 1
m.Connection(Jf,J,pos2='end')
m.Equation(J.dt() == pr*pSize)
# maximize profit
m.Obj(-Jf)

# options
m.options.IMODE = 6  # optimal control
m.options.NODES = 3  # collocation nodes
m.options.SOLVER = 1 # solver (IPOPT)

# solve optimization problem
m.solve()

# print profit
print('Optimal Profit: ' + str(Jf.value[0]))

# plot results
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(m.time,J.value,'r--',label='Bits')
plt.plot(m.time[-1],Jf.value[0],'ro',markersize=10,\
         label='final packets = '+str(Jf.value[0]))
plt.plot(m.time,nrj.value,'b-',label='energy')
plt.ylabel('Value')
plt.legend()
plt.subplot(2,1,2)
plt.plot(m.time,pr.value,'k.-',label='packet rate')
plt.ylabel('Rate')
plt.xlabel('Time (yr)')
plt.legend()
plt.show()

