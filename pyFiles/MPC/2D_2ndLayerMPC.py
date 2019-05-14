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
        
        # time points
        self.ctrlHrz = ctrlHrz                  # Control Horizon
        self.ctrlRes = ctrlRes                  # Control Resolution. Number of control steps within the control horizon
        #self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        
        # constants
        self.Egen = 1*10**-3
        self.pSize = ps        
        
        self.PERC = p
        self.nds = 40                                   # ALL NODES
        self.CHs = int(self.nds*self.PERC)              # CLUSTER HEADS
        self.nonCHs = int(self.nds - self.CHs)          # NON-CHs
        self.CHLst = []                                 # List of CH positions Param()
        self.CHxPos = []                                 # List of CH x/y positions as a Param()
        self.CHyPos = []
        self.CHdstLst = []
        self.CHdistLst = []                             # List of CHs distances Var()
        
        self.nonCHLst = []                              # List of non-CH positions Param()
        self.nonCHpos = []
        self.nonCHxPos = []
        self.nonCHyPos = []
        self.nonCHdstLst = []
        self.nonCHdistLst = []                          # List of non-CHs distances Var()
        
        self.intermeds = []                             # List of intermediate equations for energy consumption of nodes
        self.distIMCH = []                              # List of intermediate equations for distance between sink and CH
        self.distIMnonCH = []                           # List of intermediate equations for distance between sink and non-CH
        
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
        self.snkPos = [self.m.Var(value = self.sink.xPos, lb = 0, ub = 100), self.m.Var(value = self.sink.yPos, lb = 0, ub = 100)] 
        
        for i in range(len(self.CHds)):
            self.CHxPos.append(self.m.Param(value = self.CHds[i].xPos))
            self.CHyPos.append(self.m.Param(value = self.CHds[i].yPos))
            
            temp = np.sqrt((self.CHds[i].xPos)**2 + (self.CHds[i].yPos)**2)
            self.CHdstLst.append(self.m.Var(value = temp))
            
            self.m.Equation(self.CHdstLst[i] == self.m.sqrt((self.snkPos[0] - self.CHxPos[i])**2 + (self.snkPos[1] - self.CHyPos[i])**2))
        
        print('CHxPos:\n {0}'.format(self.CHxPos))
        print('CHyPos:\n {0}'.format(self.CHyPos))
        print('CHdstLst:\n {0}'.format(self.CHdstLst))
        
        for i in range(len(self.nonCHds)):
            self.nonCHxPos.append(self.m.Param(value = self.nonCHds[i].xPos))
            self.nonCHyPos.append(self.m.Param(value = self.nonCHds[i].yPos))
            
            temp = np.sqrt((self.nonCHds[i].xPos)**2 + (self.nonCHds[i].yPos)**2)
            
            self.nonCHdstLst.append(self.m.Var(value = temp))
            self.m.Equation(self.nonCHdstLst[i] == self.m.sqrt((self.snkPos[0] - self.nonCHxPos[i])**2 + (self.snkPos[1] - self.nonCHyPos[i])**2))
        
        print('nonCHxPos:\n {0}'.format(self.nonCHxPos))
        print('nonCHyPos:\n {0}'.format(self.nonCHyPos))
        print('nonCHdstLst:\n {0}'.format(self.nonCHdstLst))
        
        self.packs = 1
        self.dtrLst = []
        self.rnds = self.m.Var(integer = True, lb = 1)
        self.ECH_sum = []
        self.EnonCH_sum = []
        
        for i in range(len(self.CHds)):
            self.ECH_sum.append(self.m.Var(value = self.CHds[i].energy))
        for i in range(len(self.nonCHds)):
            self.EnonCH_sum.append(self.m.Var(value = self.nonCHds[i].energy))
        
        print('ECH_sum:\n {0}'.format(self.ECH_sum))
        print('ECH_sum:\n {0}'.format(self.m.sum(self.ECH_sum).value))
        print('EnonCH_sum:\n {0}'.format(self.EnonCH_sum))
        #self.E_tot = self.m.Param(value = 50)
        #(self.m.sum(self.ECH_sum) + self.m.sum(self.EnonCH_sum))
        self.E_total = self.m.Intermediate(self.m.sum(self.ECH_sum) + self.m.sum(self.EnonCH_sum))
        self.E_tot = self.m.Param(value = 50)
        self.e1Sum = []
        self.e2Sum = []
        
        
        for i in range(len(self.CHds)):
            self.dtrLst.append(self.m.Var(lb = 1, ub = 20))
            self.e1Sum.append(self.m.Intermediate((Eelec+EDA)*self.CHds[i].conChildren + self.dtrLst[-1]*self.pSize*(Eelec + Eamp * self.CHdstLst[i]**2)))
            self.m.Equation(self.ECH_sum[i] >= self.e1Sum[i])

        for i in range(len(self.nonCHds)):
            self.e2Sum.append(self.m.Intermediate(self.nonCHds[i].PA*self.pSize*(Eelec + Eamp * self.nonCHdstLst[i]**2)))
            self.m.Equation(self.EnonCH_sum[i] >= self.e2Sum[i])
            
            
        print('dtrLst:\n {0}'.format(self.dtrLst))
        print('e1Sum:\n {0}'.format(self.e1Sum))
        print('e2Sum:\n {0}'.format(self.e2Sum))
        
        self.m.Equation(self.E_tot >= (self.m.sum(self.e1Sum)+ self.m.sum(self.e2Sum))*self.rnds)
        
        print('E_tot:\n {0}'.format(self.E_tot.value))
        self.target = self.m.Intermediate(self.m.sum(self.dtrLst)*self.rnds)
        self.m.Obj(-self.target)        
        
        
        
        
        
        
        
        self.m.solve(disp=False)
        print('Sink X: {0}'.format(self.snkPos[0].value))
        print('Sink Y: {0}'.format(self.snkPos[1].value))
        print(self.rnds.value)
        
        
        
        """
        #WORKING SCRIPT FOR ONE DIMENSION
        
        self.sinkPos = self.m.Var(value = 30, lb=0,ub=100) # Upper bound should be something like sqrt(100**2 + 100**2)

        #self.sinkV = self.m.MV(lb=-3,ub=3)
        #self.sinkV.STATUS = 1

        # as data is transmitted, remaining data stored decreases
        
        for i in range(self.CHs):
            self.CHLst.append(self.m.Param(value = 4*i)) 
            self.CHdistLst.append(self.m.Var(value = self.sinkPos.value - self.CHLst[i].value))
            #self.distIMCH.append(self.m.Intermediate(self.sinkPos - self.CHLst[i])) 
            self.m.Equation(self.CHdistLst[i] == self.sinkPos - self.CHLst[i])
        
        for i in range(self.nonCHs):
            self.nonCHLst.append(self.m.Param(value = 2*i))
            self.nonCHdistLst.append(self.m.Var(value = self.sinkPos.value - self.nonCHLst[i].value))
            #self.distIMnonCH.append(self.m.Intermediate(self.sinkPos - self.nonCHLst[i])) 
            
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
        print(self.sinkPos.value)
        print(self.rnds.value)
        """



















        
        
    def plot(self):
        objects = np.linspace(1,len(self.CHdstLst),len(self.CHdstLst))
        print('OBJECTS: {0}'.format(objects))
        #for i in range(self.CHLst):
        #    objects.append(self.CHdistLst[i].)
            
        y_pos = np.arange(len(objects))
        ydtr = np.linspace(0,20,11)
        
        ydist = np.linspace(-50,50,11)
        
        CHDL = []
        for i in range(len(self.CHdstLst)):
            CHDL.append(self.CHdstLst[i][0])
        
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
        
        """
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
        """
    def clearGEKKO(self):
        self.m.clear()


if __name__ == "__main__":
    Hrz = 8
    Res = Hrz + 1
    
    testEnv = MPC2ndLayer(Hrz,Res)
    testEnv.cluster()
    print('Amount of Cluster Heads: {0}'.format(len(testEnv.CHds)))

    
    testEnv.controlEnv()
    testEnv.plot()
    