# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:36:10 2019

@author: axkar1
"""

from gekko import GEKKO
import numpy as np
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from EnvironmentEngine import EnvironmentEngine
from setParams import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt


class MPC2ndLayer(EnvironmentEngine):
    def __init__(self, ctrlHrz, ctrlRes):
        super().__init__()  
        
        self.verbose = False
        self.nrplots = 0
         
         
        self.m = GEKKO(remote=False)
        
        # time points
        self.ctrlHrz = ctrlHrz                  # Control Horizon
        self.ctrlRes = ctrlRes                  # Control Resolution. Number of control steps within the control horizon
        #self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        
        # constants
        self.Egen = 1*10**-3
        self.const = 0.6
        self.packet = 1
        self.pSize = ps        
        
        
        
        self.PERC = 0.10
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
    
        self.sinkPos = self.m.Var(value = 30, lb=0,ub=100) # Upper bound should be something like sqrt(100**2 + 100**2)
        #self.sinkPos.STATUS = 1
        
        #self.sinkV = self.m.MV(lb=-3,ub=3)
        #self.sinkV.STATUS = 1
        
        
        # define distance 
        for i in range(self.CHs):
            self.CHLst.append(self.m.Param(value = 4*i)) 
            self.CHdistLst.append(self.m.Var(value = self.sinkPos.value - self.CHLst[i].value))
            self.distIMCH.append(self.m.Intermediate(self.sinkPos - self.CHLst[i])) 
            self.m.Equation(self.CHdistLst[i] == self.sinkPos - self.CHLst[i])
            
        for i in range(self.nonCHs):
            self.nonCHLst.append(self.m.Param(value = 2*i))
            self.nonCHdistLst.append(self.m.Var(value = self.sinkPos.value - self.nonCHLst[i].value))
            self.distIMnonCH.append(self.m.Intermediate(self.sinkPos - self.nonCHLst[i])) 
            
            self.m.Equation(self.nonCHdistLst[i] == self.sinkPos - self.nonCHLst[i])
            
        print(self.nonCHLst[1].value)
        print(self.sinkPos.value)
        
        
        # as data is transmitted, remaining data stored decreases

        
        # energy to transmit
        #self.packs = self.m.Param()
        self.packs = 1
        self.dtrLst = []
        self.rnds = self.m.Var(lb = 1)
        self.E_tot = self.m.Param(value = 0.005)
        self.data = self.m.Var(value = 0)
        self.e1Sum = []
        self.e2Sum = []
        
        
        for i in range(self.CHs):
            #self.intermeds.append(self.m.Intermediate((Eelec+EDA)*self.packet + self.packs*self.pSize*(Eelec + Eamp * self.CHdistLst[i]**2)))  
            #self.intermeds.append(self.m.Intermediate(self.E_tot/((Eelec+EDA)*self.packet + self.dtrLst[-1]*self.pSize*(Eelec + Eamp * self.CHdistLst[i]**2))))
            #self.m.Obj(-self.intermeds[-1])
            self.dtrLst.append(self.m.Var(lb = 1, ub = 20))
            self.e1Sum.append(self.m.Intermediate((Eelec+EDA)*self.packs + self.dtrLst[-1]*self.pSize*(Eelec + Eamp * self.CHdistLst[i]**2)))
            

        for i in range(self.nonCHs):
            #self.intermeds.append(self.m.Intermediate(self.packs*self.pSize*(Eelec + Eamp * self.nonCHdistLst[i]**2)))  
            #self.intermeds.append(self.m.Intermediate(self.E_tot/(self.packs*self.pSize*(Eelec + Eamp * self.nonCHdistLst[i]**2))))
            #self.m.Obj(-self.intermeds[-1])
            self.e2Sum.append(self.m.Intermediate(self.packs*self.pSize*(Eelec + Eamp * self.nonCHdistLst[i]**2)))
            
        
        
        
        self.dm1 = np.sum(self.CHdistLst)/len(self.CHdistLst)            # Mean distance of CH to sink
        self.dm2 = np.sum(self.nonCHdistLst)/len(self.nonCHdistLst)      # Mean distance of nonCH to sink
        
        self.e1 = self.m.Intermediate(((Eelec+EDA)*self.packet + self.packs*self.pSize*(Eelec + Eamp * self.dm1**2))*len(self.CHdistLst)) # Mean energy consumption per round for CHs
        self.e2 = self.m.Intermediate((self.packs*self.pSize*(Eelec + Eamp * self.dm2**2))*len(self.nonCHdistLst)) # Mean energy consumption per round for CHs
        
        
        
        self.rnd = self.m.Intermediate(self.E_tot/(self.PERC*self.E_tot*self.e1+(1-self.PERC)*self.e2))
        #self.m.Equation(self.data == self.m.sum(self.dtrLst)*self.rnd)
        self.m.Equation(self.E_tot >= (self.m.sum(self.e1Sum)+ self.m.sum(self.e2Sum))*self.rnds)
        self.target = self.m.Intermediate(self.m.sum(self.dtrLst)*self.rnds)
        self.m.Obj(-self.target)
        
        
        
        # options
        self.m.options.IMODE = 3                 # optimize a solid state

        
        
        

    def controlEnv(self):
        self.m.solve()
        print(self.sinkPos.value)
        print(self.rnd.value)
        print(self.data.value)
        
        
    def plot(self):
        
        N = len(self.dtrLst)
        
        x = range(N)
        
        objects = np.linspace(1,len(self.CHLst),1)
        #for i in range(self.CHLst):
        #    objects.append(self.CHdistLst[i].)
            
        y_pos = np.arange(len(objects))
        
        CHDL = []
        for i in range(len(self.CHdistLst)):
            CHDL.append(self.CHdistLst.value.value[i])
        
        DTRL = []
        for i in range(len(self.dtrLst)):
            DTRL.append(self.dtrLst.value.value[i])
        
        plt.figure(self.nrplots)
        plt.subplot(2,1,1)
        plt.barh(y_pos, self.CHDL, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.xlabel('distance')
        plt.title('Node#')
        
        
        plt.figure(self.nrplots)
        plt.subplot(2,1,2)
        plt.barh(y_pos, self.DTRL, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.xlabel('packets desired')
        plt.title('Node#')
        
        
        plt.show()
        """
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
    def clearGEKKO(self):
        self.m.clear()


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
    testEnv.plot()
    