# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:48:16 2019

@author: axkar1
"""

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
PRmax = 2000
const = 0.6

packet = 1
E = 1

# packet rate
pr = m.MV(value=1,lb=0,ub=1)
pr.STATUS = 1
pr.DCOST = 0

packets = m.CV(value=0)
# Energy Stored
nrj = m.Var(value=0.005, lb=0)                  # Energy Amount
d = m.Var(value=70, lb = 0)                     # Distance to receiver
d2 = m.Intermediate(d**2)


# energy/pr balance
m.Equation(d.dt() == -0.5)
m.Equation(nrj >= Egen - ((Eelec+EDA)*packet + pr*PRmax*(Eelec + Eamp * d2)))
m.Equation(nrj.dt() == Egen - ((Eelec+EDA)*packet + pr*PRmax*(Eelec + Eamp * d2)))


# objective (profit)
J = m.Var(value=0)
# final objective
Jf = m.FV()
Jf.STATUS = 1
m.Connection(Jf,J,pos2='end')
m.Equation(J.dt() == pr*PRmax)
# maximize profit
m.Obj(-Jf)

# options
m.options.IMODE = 6  # optimal control
m.options.NODES = 3  # collocation nodes
m.options.SOLVER = 3 # solver (IPOPT)

# solve optimization problem
m.solve()

# print profit
print('Optimal Profit: ' + str(Jf.value[0]))

# plot results
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(m.time,J.value,'r--',label='packets')
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