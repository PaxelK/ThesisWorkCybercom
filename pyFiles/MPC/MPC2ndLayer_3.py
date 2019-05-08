# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:36:10 2019

@author: axkar1
"""

from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from EnvironmentEngine import EnvironmentEngine
from setParams import *

class MPC2ndLayer(EnvironmentEngine):
    def __init__(self, ctrlHrz, ctrlRes):
        super().__init__()  
        
        self.verbose = False
        self.nrplots = 0
         
         
        self.m = GEKKO(remote=False)
        
        # time points
        self.ctrlHrz = ctrlHrz                  # Control Horizon
        self.ctrlRes = ctrlRes                  # Control Resolution. Number of control steps within the control horizon
        self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        
        # constants
        self.Egen = 1*10**-3
        self.const = 0.6
        self.packet = 1
        self.pSize = ps        
        
        self.PERC = 0.05
        self.PERCREV = 1 - self.PERC
        
        #Counter for plots
        self.nrplots = 1;
    
        
        self.nds = 20                          # ALL NODES
        self.CHs = self.nds*self.PERC           # CLUSTER HEADS
        self.nonCHs = self.nds*self.PERCREV     # NON-CHs
        
    
    
        # define total energy
        totnrj = 1
        self.Etot = self.m.Var(value = totnrj)
        
        # define distance 
        
         
        # Define node positions
        self.sinkPos = self.m.MV(lb=0,ub=100) # Upper bound should be something like sqrt(100**2 + 100**2)
        self.sinkPos.STATUS = 1 
        
        
        self.CHLst = []
        self.CHdistLst = []
        for i in range(self.CHLst):
            self.CHLst.append(self.m.Var(value = 3*i)) 
            self.CHdistLst.append(self.m.Var())
            self.m.Equation(self.CHdistLst(i) == self.sinkPos - self.CHLst(i))
            
        self.nonCHLst = []
        self.nonCHdistLst = []
        for i in range(self.nonCHLst):
            self.nonCHLst.append(self.m.Var(value = 2*i))
            self.nonCHdistLst.append(self.m.Var())
            self.m.Equation(self.nonCHdistLst(i) == self.sinkPos - self.nonCHLst(i))
            
        #for i in range(self.nds):    
            
        
        #self.nodePos = self.m.Var(value = 20)
        #self.nodePos1 = self.m.Var(value = 40)
        
        
        
        self.sinkd = self.m.Var()
        self.sinkd1 = self.m.Var()
        
        self.m.Equation(self.sinkd1 == self.sinkPos - self.nodePos1)
        
        self.dm = self.m.Intermediate((self.sinkd + self.sinkd1)/2)
        
        
        #define energyloss for CHs and nodes
        self.e = self.m.Intermediate(((Eelec+EDA)*self.packs + self.packs*self.pSize*(Eelec + Eamp * self.dist**2)) - self.Egen)
        self.es = self.m.Intermediate(self.packs*self.pSize*(Eelec + Eamp * self.sinkd**2))
        
       
        
        
         
        
        
        # define data transmission rate
        self.packs = self.m.MV(integer = True, lb=0,ub=200)
        self.packs.STATUS = 1
        
        self.packs1 = self.m.MV(integer = True, lb=0,ub=200)
        self.packs1.STATUS = 1
        
         # energy to transmit
        self.e = self.m.Intermediate(self.packs*self.pSize*(Eelec + Eamp * self.sinkd**2))
        self.e1 = self.m.Intermediate(self.packs1*self.pSize*(Eelec + Eamp * self.sinkd1**2))
        
        # energy dissipation
        self.nrj = self.m.Var(value = 0.05, lb = 0)
        self.nrj1 = self.m.Var(value = 0.035, lb = 0)
        
        self.m.Equation(self.nrj.dt() == -self.packs1*self.pSize*(Eelec + Eamp * self.sinkd**2))
        self.m.Equation(self.nrj1.dt() == -self.packs1*self.pSize*(Eelec + Eamp * self.sinkd1**2))
        
        
        self.data= self.m.Var()
        
        
        # equations
        
        
        # as data is transmitted, remaining data stored decreases
        self.m.Equation(self.data.dt() == self.packs + self.packs1)
        
        
        
         # soft (objective constraint)
        self.final = self.m.Param(value=np.zeros(self.ctrlRes))
        self.final.value[int(np.floor(self.ctrlRes/2)):-1] = 0.001
        self.final.value[-1] = 1
        
        self.m.Equation(self.final*(self.data)>=0)
        
        # objective
        Q = 1
        R = 1
        self.j = self.m.Intermediate(-Q*self.nrj + R*self.e)
        self.j1 = self.m.Intermediate(-Q*self.nrj1 + R*self.e1)
        
        self.jBalance = self.m.Intermediate(-self.nrj/self.e)
        self.jBalance1 = self.m.Intermediate(-self.nrj1/self.e1)
        
        self.m.Obj(self.j + self.j1)
        self.m.Obj(self.jBalance + self.jBalance1)
        
        #self.m.Obj(self.nrj/self.e) # minimize energy
        #self.m.Obj(self.nrj1/self.e1) # minimize energy
        self.m.Obj(-self.data*self.final)
        
        #self.j = self.m.Intermediate(self.nrj/self.e)
        #self.j1 = self.m.Intermediate(self.nrj1/self.e1)
        
        self.E = 1
        self.c = 0.03
        #self.m.Obj(-(self.E-self.c/0.05)*self.data)
        #self.m.Obj(-((self.j+self.j1-2)*self.data)
                
        # options
        self.m.options.IMODE = 6                # optimal control
        self.m.options.NODES = 3                # collocation nodes
        self.m.options.SOLVER = 1               # solver (IPOPT), 1 is for when integers is used as MV
        self.m.options.TIME_SHIFT = 1           # Setting for saving values from last solve()



       
        
        """
        m.Equation(x.dt() == r*x*(1-x/k)-u*U_max)
        # objective (profit)
        J = m.Var(value=0)
        # final objective
        Jf = m.FV()
        Jf.STATUS = 1
        m.Connection(Jf,J,pos2='end')
        m.Equation(J.dt() == (E-c/x)*u*U_max)
        """

    def controlEnv(self):
        self.m.solve()
        
    def plot(self):
        plt.figure(self.nrplots)
        plt.subplot(6,1,1)
        plt.plot(self.m.time,self.sinkd.value,'r-',label='Distance')
        plt.legend()
        
        plt.figure(self.nrplots)
        plt.subplot(6,1,2)
        plt.plot(self.m.time,self.sinkd1.value,'r-',label='Distance')
        plt.legend()
        
        #plt.subplot(7,1,3)
        #plt.plot(self.m.time,self.v.value,'k--',label='Velocity')
        #plt.legend()
        
        plt.subplot(6,1,3)
        plt.plot(self.m.time,self.e.value,'b-',label='Energy Consumption')
        plt.legend()
        
        #plt.subplot(6,1,3)
        #plt.plot(self.m.time,self.ps,'b-',label='Bits Sent')
        #plt.legend()
        
        plt.subplot(6,1,4)
        plt.plot(self.m.time, self.data.value,'k.-',label='Data Sent')
        plt.legend()
        
        
        plt.subplot(6,1,5)
        plt.plot(self.m.time, self.packs.value,'r-',label='Transmission Amount, packs')
        plt.legend()
        
        plt.subplot(6,1,6)
        plt.plot(self.m.time, self.packs1.value,'r-',label='Transmission Amount1, packs1')
        plt.legend()
        
        #plt.subplot(6,1,6)
        #plt.plot(self.m.time,self.nrj_stored,'b-',label='Battery')
        #plt.legend()
        #plt.xlabel('Time')
        
        self.nrplots+=1
        
        
        
"""    
             
    
    def controlPR(self, velocity):  
        temp = np.float64(velocity)
        
        self.vp[0:] = self.v.value[1]
        if(temp == self.vp[0]):
            if self.verbose:
                print('Velocity: {0} was equal to vVal0: {1}'.format(temp, self.vp[0]))
                print('Therefore, velocity was set as vp[1:]')
        else:
            if self.verbose:
                print('Velocity: {0} was not equal to vVal0: {1}'.format(temp, self.v.value[0]))
                print('Therefore, vp[1:] was set as tempVel = {0}'.format(temp))
            self.vp[1:] = temp 
            #print(self.vp)
                
        self.v.value = self.vp
            #print(np.shape(testNode.vp))  
        if(type(self.dtr.value.value) is not int):
            self.dtrp = np.zeros(self.ctrlRes)
            self.dtrp[0] = self.dtr.value[1]
            self.dtr.value = self.dtrp
            
            #self.nrj_stored.value[0] = self.nrj_stored.value[1]
            #self.data.value[0] = self.data.value[1]
        

        #self.data.value[0] = self.data.value[1]
        self.m.solve(disp=False) # solve optimization problem
        self.setPR(self.dtr.value[0])
        
    def clearGEKKO(self):
        self.m.clear()

"""
if __name__ == "__main__":
    Hrz = 8
    Res = Hrz + 1
    
    testEnv = MPC2ndLayer(Hrz,Res)
   # print(testEnv.sink.xPos)
    #print(testEnv.ctrlHrz)
    testEnv.nodes[0].energy = 0.05
    for node in testEnv.nodes:
        print(node.energy)
        
    testEnv.controlEnv()
    testEnv.plot()
        
        
