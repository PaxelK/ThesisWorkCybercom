# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:46:43 2019

@author: axkar1
"""

from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from Node import Node
import Sink
from setParams import *

class MPCnode(Node):
    def __init__(self, id, x, y, nrj, ctrlHrz, ctrlRes):
        super().__init__(id, x, y, nrj)  
        
        self.verbose = True
        
        self.ctrlHrz = ctrlHrz                  # Control Horizon
        
        # time points
        self.ctrlRes = ctrlRes                  # Control Resolution. Number of control steps within the control horizon
        # constants
        self.Egen = 1*10**-5
        self.const = 0.6
        
        self.packet = 1
        self.E = 1
        
        self.m = GEKKO(remote=False)
        self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        
        
        
        #self.deltaDist = -1.5
        self.deltaDist = self.m.FV(value = -1.5)
        #self.deltaDist.STATUS = 1

                # packet rate
        self.pr = self.m.MV(value=self.PA, integer = True,lb=1,ub=20)
        self.pr.STATUS = 1
        self.pr.DCOST = 0
        
        # Energy Stored
        self.nrj = self.m.Var(value=0.05, lb=0)                  # Energy Amount
        self.d = self.m.Var(value=70, lb = 0)                     # Distance to receiver
        self.d2 = self.m.Intermediate(self.d**2)
        
        
        
        # energy/pr balance
        #self.m.Equation(self.d.dt() == -1.5)
        self.m.Equation(self.d.dt() == self.deltaDist)
        self.m.Equation(self.nrj >= self.Egen - ((Eelec+EDA)*self.packet + self.pr*self.pSize*(Eelec + Eamp * self.d2)))
        self.m.Equation(self.nrj.dt() == self.Egen - ((Eelec+EDA)*self.packet + self.pr*self.pSize*(Eelec + Eamp * self.d2)))
        
        
        # objective (profit)
        self.J = self.m.Var(value=0)
        # final objective
        self.Jf = self.m.FV()
        self.Jf.STATUS = 1
        self.m.Connection(self.Jf,self.J,pos2='end')
        self.m.Equation(self.J.dt() == self.pr*self.pSize)
        # maximize profit
        self.m.Obj(-self.Jf)
        
        # options
        self.m.options.IMODE = 6  # optimal control
        self.m.options.NODES = 3  # collocation nodes
        self.m.options.SOLVER = 1 # solver (IPOPT)



    def getDeltaDist(self, sinkX, sinkY, sdeltaX, sdeltaY, deltaDist):        
        distBefore = np.sqrt((sinkX**2)+(sinkY**2))
        distAfter = np.sqrt(((sinkX+sdeltaX)**2)+((sinkY+sdeltaY)**2))
        self.deltaDist = distAfter - distBefore
        return self.deltaDist
    
    def controlPR(self, deltaD):        

        
        # solve optimization problem
        self.deltaDist.value = 1.5

        self.m.solve(disp=False)
        
        self.setPR(self.pr.value[1])
        #self.pr.value = self.pr.value[1]
        
        #self.m.GUI()
        
        # print profit
        print('Optimal Profit: ' + str(self.Jf.value[0]))
        
        if self.verbose:
            # plot results
            plt.figure(1)
            plt.subplot(2,1,1)
            plt.plot(self.m.time,self.J.value,'r--',label='packets')
            plt.plot(self.m.time[-1],self.Jf.value[0],'ro',markersize=10,\
                     label='final packets = '+str(self.Jf.value[0]))
            plt.plot(self.m.time,self.nrj.value,'b-',label='energy')
            plt.ylabel('Value')
            plt.legend()
            plt.subplot(2,1,2)
            plt.plot(self.m.time,self.pr.value,'k.-',label='packet rate')
            plt.ylabel('Rate')
            plt.xlabel('Time (yr)')
            plt.legend()
            plt.show()


if __name__ == "__main__":
    testNode = MPCnode(1,20,20,15,10,11)
    dist = 70
    """
    for i in range(5):
        testNode.controlPR(-0.5)
        print(testNode.PA)
    """
    for i in range(1):
        testNode.controlPR(-1.5)
        print(testNode.PA)



'''


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
'''