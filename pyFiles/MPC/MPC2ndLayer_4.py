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
        
        
        
        self.PERC = 0.4
        self.nds = 30                                   # ALL NODES
        self.CHs = int(self.nds*self.PERC)              # CLUSTER HEADS
        self.nonCHs = int(self.nds - self.CHs)          # NON-CHs
        self.CHLst = []                                 # List of CH positions Param()
        self.CHdistLst = []                             # List of CHs distances Var()
        
        self.nonCHLst = []                              # List of non-CH positions Param()
        self.nonCHdistLst = []                          # List of non-CHs distances Var()
        
        self.intermeds = []                             # List of intermediate equations for energy consumption of nodes
        self.distIMCH = []                              # List of intermediate equations for distance between sink and CH
        self.distIMnonCH = []                           # List of intermediate equations for distance between sink and non-CH
        
        #Counter for plots
        self.nrplots = 1;
    
        self.sinkPos = self.m.Var(lb=0,ub=100) # Upper bound should be something like sqrt(100**2 + 100**2)
        #self.sinkPos.STATUS = 1
        
        #self.sinkV = self.m.MV(lb=-3,ub=3)
        #self.sinkV.STATUS = 1
    
        # define distance 
        for i in range(self.CHs):
            self.CHLst.append(self.m.Param(value = 4*i)) 
            self.CHdistLst.append(self.m.Var(value = self.sinkPos - self.CHLst[i]))
            self.distIMCH.append(self.m.Intermediate(self.sinkPos - self.CHLst[i])) 
            
            self.m.Equation(self.CHdistLst[i] == self.sinkPos - self.CHLst[i])
            #self.m.Equation(self.CHdistLst[i].dt() == (self.m.abs(self.distIMCH[i])/self.distIMCH[i])*self.sinkV)
        
        for i in range(self.nonCHs):
            self.nonCHLst.append(self.m.Param(value = 2*i))
            self.nonCHdistLst.append(self.m.Var(value = self.sinkPos - self.nonCHLst[i]))
            self.distIMnonCH.append(self.m.Intermediate(self.sinkPos - self.nonCHLst[i])) 
            
            self.m.Equation(self.nonCHdistLst[i] == self.sinkPos - self.nonCHLst[i])
            #self.m.Equation(self.nonCHdistLst[i].dt() == (self.m.abs(self.distIMnonCH[i])/self.distIMnonCH[i])*self.sinkV)
        
        print(self.nonCHLst[1].value)
        print(self.sinkPos.value)
        
        
        # as data is transmitted, remaining data stored decreases
        #self.m.Equation(self.data.dt() == self.packs + self.packs1)
        
        # energy to transmit
        self.packs = 1
        for i in range(self.CHs):
            self.intermeds.append(self.m.Intermediate((Eelec+EDA)*self.packet + self.packs*self.pSize*(Eelec + Eamp * self.CHdistLst[i]**2)))  
            self.m.Obj(self.intermeds[i])
        for i in range(self.nonCHs):
            self.intermeds.append(self.m.Intermediate(self.packs*self.pSize*(Eelec + Eamp * self.nonCHdistLst[i]**2)))  
            self.m.Obj(self.intermeds[i])
        
        
        self.dm1 = np.sum(self.CHdistLst)/len(testEnv.CHdistLst)            # Mean distance of CH to sink
        self.dm2 = np.sum(self.nonCHdistLst)/len(testEnv.nonCHdistLst)      # Mean distance of nonCH to sink
        
        self.e1 = self.m.Intermediate((Eelec+EDA)*self.packet + self.packs*self.pSize*(Eelec + Eamp * self.dm1**2)) # Mean energy consumption per round for CHs
        self.e2 = self.m.Intermediate((Eelec+EDA)*self.packet + self.packs*self.pSize*(Eelec + Eamp * self.dm2**2)) # Mean energy consumption per round for CHs
        
        self.E_tot = self.m.Var(value = 1)
        self.round = self.m.Var()
        
        self.rnd = self.m.Intermediate(self.E_tot/(self.PERC*self.E_tot*self.e1+(1-self.PERC)*self.e2))
        
        self.m.Obj(-self.rnd)
        
        """
        self.data = self.m.Var()
        for i in range(self.intermeds):
            self.
        self.m.Equation(self.data.dt() == self.packs*self.pSize + self.dtr1*self.pSize)
        
        
        
         # soft (objective constraint)
        self.final = self.m.Param(value=np.zeros(self.ctrlRes))
        self.final.value[int(np.floor(self.ctrlRes/2)):-1] = 0.001
        self.final.value[-1] = 1
        
        self.m.Equation(self.final*(self.data)>=0)
        
        # objective
        self.m.Obj(self.e) # minimize energy
        self.m.Obj(self.e1) # minimize energy
        self.m.Obj(-self.data*self.final)
        """
        
        
        # options
        self.m.options.IMODE = 3                # optimal control
        #self.m.options.NODES = 3                # collocation nodes
        #self.m.options.SOLVER = 1               # solver (IPOPT), 1 is for when integers is used as MV
        #self.m.options.TIME_SHIFT = 1           # Setting for saving values from last solve()

        
        
        

    def controlEnv(self):
        self.m.solve()
        print(self.sinkPos.value)
        print(self.rnd.value)
        
    def plot(self):
        plt.figure(self.nrplots)
        plt.subplot(4,1,1)
        plt.plot(self.m.time,self.CHdistLst[6].value,'r-',label='Distance')
        plt.legend()
        
        plt.figure(self.nrplots)
        plt.subplot(4,1,2)
        plt.plot(self.m.time,self.CHdistLst[7].value,'r-',label='Distance')
        plt.legend()
        
        #plt.subplot(7,1,3)
        #plt.plot(self.m.time,self.v.value,'k--',label='Velocity')
        #plt.legend()
        
        plt.subplot(4,1,3)
        plt.plot(self.m.time,self.intermeds[0].value,'b-',label='Energy Consumption')
        plt.legend()
        
        #plt.subplot(6,1,3)
        #plt.plot(self.m.time,self.ps,'b-',label='Bits Sent')
        #plt.legend()
        
        plt.subplot(4,1,4)
        plt.plot(self.m.time, self.sinkV.value,'k.-',label='Sink Vel')
        plt.legend()
        
        
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
    #for node in testEnv.nodes:
        #print(node.energy)
        
    testEnv.controlEnv()
    #testEnv.plot()
    