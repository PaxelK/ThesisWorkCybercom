# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:36:10 2019

@author: axkar1
"""

from gekko import GEKKO
import numpy as np
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from EnvironmentEngineMPC import EnvironmentEngineMPC
from setParamsMPC import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt


class MPC2ndLayer(EnvironmentEngineMPC):
    def __init__(self, ctrlHrz, ctrlRes):
        super().__init__()  
        
        self.verbose = False
        self.nrplots = 0
         
         
        self.m = GEKKO(remote=False)
        #self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        
        # constants
        self.Egen = 1*10**-3
        self.pSize = ps        
        
        self.PERC = p
        self.nds = 40                                   # ALL NODES
        self.CHs = int(self.nds*self.PERC)              # CLUSTER HEADS
        self.nonCHs = int(self.nds - self.CHs)          # NON-CHs
        self.CHLst = []                                 # List of CH positions Param()
        self.CHdistLst = []                             # List of CHs distances Var()
        
        self.nonCHLst = []                              # List of non-CH positions Param()
        self.nonCHpos = []
        self.nonCHdistLst = []                          # List of non-CHs distances Var()
        
        self.intermeds = []                             # List of intermediate equations for energy consumption of nodes

        #Counter for plots
        self.nrplots = 1;
    
        

        

        
        """
        This part is in case the LEACH protocol is to be used in the model.
        self.dm1 = np.sum(self.CHdistLst)/len(self.CHdistLst)            # Mean distance of CH to sink
        self.dm2 = np.sum(self.nonCHdistLst)/len(self.nonCHdistLst)      # Mean distance of nonCH to sink
        
        self.e1 = self.m.Intermediate(((Eelec+EDA)*self.packet + self.packs*self.pSize*(Eelec + Eamp * self.dm1**2))*len(self.CHdistLst)) # Mean energy consumption per round for CHs
        self.e2 = self.m.Intermediate((self.packs*self.pSize*(Eelec + Eamp * self.dm2**2))*len(self.nonCHdistLst)) # Mean energy consumption per round for CHs
        
        self.rnd = self.m.Intermediate(self.E_tot/(self.PERC*self.E_tot*self.e1+(1-self.PERC)*self.e2))
        """
        
        # options
        self.m.options.IMODE = 3                 # optimize a solid state

        
        
        

    def controlEnv(self):

        #WORKING SCRIPT FOR ONE DIMENSION
        
        self.sinkPos = self.m.Var(value = 30, lb=0,ub=100) # Upper bound should be something like sqrt(100**2 + 100**2)

        #self.sinkV = self.m.MV(lb=-3,ub=3)
        #self.sinkV.STATUS = 1

        # as data is transmitted, remaining data stored decreases
        
        for i in range(self.CHs):
            self.CHLst.append(self.m.Param(value = 4*i)) 
            self.CHdistLst.append(self.m.Var(value = self.sinkPos.value - self.CHLst[i].value))
            self.m.Equation(self.CHdistLst[i] == self.sinkPos - self.CHLst[i])
        
        for i in range(self.nonCHs):
            self.nonCHLst.append(self.m.Param(value = 2*i))
            self.nonCHdistLst.append(self.m.Var(value = self.sinkPos.value - self.nonCHLst[i].value)) 
            
            self.m.Equation(self.nonCHdistLst[i] == self.sinkPos - self.nonCHLst[i])

        
        self.packs = 1
        self.dtrLst = []
        self.rnds = self.m.Var(integer = True, lb = 1)
        self.E_tot = self.m.Param(value = 3)
        self.e1Sum = []
        self.e2Sum = []
        
        
        for i in range(self.CHs):
            self.dtrLst.append(self.m.Var(lb = 1, ub = 20))
            self.e1Sum.append(self.m.Intermediate((Eelec+EDA)*self.packs + self.dtrLst[-1]*self.pSize*(Eelec + Eamp * self.CHdistLst[i]**2)))
            

        for i in range(self.nonCHs):
            self.e2Sum.append(self.m.Intermediate(self.packs*self.pSize*(Eelec + Eamp * self.nonCHdistLst[i]**2)))
                
        
        
        self.m.Equation(self.E_tot >= (self.m.sum(self.e1Sum)+ self.m.sum(self.e2Sum))*self.rnds)
        self.target = self.m.Intermediate(self.m.sum(self.dtrLst)*self.rnds)
        self.m.Obj(-self.target)

        
        self.m.solve(disp=False)
        print('Sink\'s optimal Position: {0}'.format(self.sinkPos.value))
        print('Number of rounds for optimal amount of data transmitted: {0}'.format(self.rnds.value))




        
        
    def plot(self):
        #WORKING CODE
        objects = np.linspace(1,len(self.CHLst),len(self.CHLst))
        #for i in range(self.CHLst):
        #    objects.append(self.CHdistLst[i].)
            
        y_pos = np.arange(len(objects))
        ydtr = np.linspace(0,20,11)
        
        ydist = np.linspace(-50,50,11)
        
        CHDL = []
        for i in range(len(self.CHdistLst)):
            CHDL.append(self.CHdistLst[i][0])
        
        DTRL = []
        for i in range(len(self.dtrLst)):
            DTRL.append(self.dtrLst[i][0])
        
        plt.figure(self.nrplots)
        plt.subplot(2,1,1)
        plt.bar(y_pos, CHDL, align='center', alpha=0.5)
        plt.yticks(ydist, ydist)
        plt.ylabel('distance')
        
        
        plt.subplot(2,1,2)
        plt.bar(y_pos, DTRL, align='center', alpha=0.5)
        plt.yticks(ydtr, ydtr)
        plt.ylabel('Packets Desired')
        plt.xlabel('Node#')
        
        plt.show()

    def clearGEKKO(self):
        self.m.clear()


if __name__ == "__main__":
    Hrz = 8
    Res = Hrz + 1
    testEnv = MPC2ndLayer(Hrz,Res) 
    testEnv.controlEnv()
    testEnv.plot()
    