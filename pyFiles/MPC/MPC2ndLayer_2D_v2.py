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
import pylab as pl
from MPCsink import MPCsink
from shutil import rmtree

class MPC2ndLayer(EnvironmentEngineMPC):
    def __init__(self, ctrlHrz, ctrlRes):
        super().__init__(ctrlHrz, ctrlRes)  
        
        self.verbose = False
    
        #self.resetGEKKO()
        # time points
        self.ctrlHrz = ctrlHrz                  # Control Horizon
        self.ctrlRes = ctrlRes                  # Control Resolution. Number of control steps within the control horizon
        #self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        
        # constants
        self.Egen = 1*10**-3
        self.pSize = ps        
        
        self.PERC = p
        
        self.expLifetime = 0
        self.errorFlag = False
        #Counter for plots
        self.nrplots = 1;
        
        


    def controlEnv(self):
        self.resetGEKKO()
        self.snkPos = [self.m.Var(value = self.sink.xPos, lb = 0, ub = xSize), self.m.Var(value = self.sink.yPos, lb = 0, ub = ySize)] 
        #self.snkPos = [self.m.Param(value = 50), self.m.Param(value = 50)]
        
        for i in range(len(self.CHds)):
            self.CHxPos.append(self.m.Param(value = self.CHds[i].xPos))
            self.CHyPos.append(self.m.Param(value = self.CHds[i].yPos))
            
            temp = np.sqrt((self.CHds[i].xPos)**2 + (self.CHds[i].yPos)**2)
            self.CHdstLst.append(self.m.Var(value = temp))
            
            self.m.Equation(self.CHdstLst[i] == self.m.abs2(self.m.sqrt((self.snkPos[0] - self.CHxPos[i])**2 + (self.snkPos[1] - self.CHyPos[i])**2)))
        
        if self.verbose:
            print('CHxPos:\n {0}'.format(self.CHxPos))
            print('CHyPos:\n {0}'.format(self.CHyPos))
            print('CHdstLst:\n {0}'.format(self.CHdstLst))
        
        
        
        for nch in self.nonCHds:
            if(type(nch.CHparent) is MPCsink):
                self.freeNonCHds.append(nch)
            
        for i in range(len(self.freeNonCHds)):
            self.nonCHxPos.append(self.m.Param(value = self.freeNonCHds[i].xPos))
            self.nonCHyPos.append(self.m.Param(value = self.freeNonCHds[i].yPos))
                
            temp = np.sqrt((self.freeNonCHds[i].xPos)**2 + (self.freeNonCHds[i].yPos)**2)
                
            self.nonCHdstLst.append(self.m.Var(value = temp))
            self.m.Equation(self.nonCHdstLst[i] == self.m.abs2(self.m.sqrt((self.snkPos[0] - self.nonCHxPos[i])**2 + (self.snkPos[1] - self.nonCHyPos[i])**2)))
        
        if self.verbose:
            print('nonCHxPos:\n {0}'.format(self.nonCHxPos))
            print('nonCHyPos:\n {0}'.format(self.nonCHyPos))
            print('nonCHdstLst:\n {0}'.format(self.nonCHdstLst))
        

        self.rnds = self.m.Var(lb = 0, integer = True)

        
        for i in range(len(self.CHds)):
            self.ECH_sum.append(self.m.Var(value = self.CHds[i].energy))
        for i in range(len(self.freeNonCHds)):
            self.EnonCH_sum.append(self.m.Var(value = self.freeNonCHds[i].energy))
        
        if self.verbose:
            print('ECH_sum:\n {0}'.format(self.ECH_sum))
            print('ECH_sum:\n {0}'.format(self.m.sum(self.ECH_sum).value))
            print('EnonCH_sum:\n {0}'.format(self.EnonCH_sum))


        
        E_temp = 0
        for n in self.CHds:
            E_temp += n.energy
        for nf in self.freeNonCHds:
            E_temp += nf.energy
        self.E_tot = self.m.Param(value = E_temp)
        
        for i in range(len(self.CHds)):
            self.dtrLst.append(self.m.Var(lb = 1, ub = 20))
            self.e1Sum.append(self.m.Intermediate((Eelec+EDA)*self.CHds[i].conChildren + self.dtrLst[-1]*self.pSize*(Eelec + Eamp * self.CHdstLst[i]**2)))
            self.m.Equation(self.ECH_sum[i] >= self.e1Sum[i])
        for i in range(len(self.freeNonCHds)):
            #self.e2Sum.append(self.m.Intermediate(self.freeNonCHds[i].PA*self.pSize*(Eelec + Eamp * self.nonCHdstLst[i]**2)))
            self.e2Sum.append(self.m.Intermediate(1*self.pSize*(Eelec + Eamp * self.nonCHdstLst[i]**2)))

            self.m.Equation(self.EnonCH_sum[i] >= self.e2Sum[i])
            
        if self.verbose:
            print('dtrLst:\n {0}'.format(self.dtrLst))
            print('e1Sum:\n {0}'.format(self.e1Sum))
            print('e2Sum:\n {0}'.format(self.e2Sum))
            print('E_tot:\n {0}'.format(self.E_tot.value))
         
        #self.m.Equation(self.E_tot >= (self.m.sum(self.e1Sum) + self.m.sum(self.e2Sum))*self.rnds)
        self.m.Equation(self.E_tot >= (self.m.sum(self.e1Sum) + self.m.sum(self.e2Sum))*self.rnds)

        
        self.target = self.m.Intermediate(self.m.sum(self.dtrLst)*(self.rnds-1))
        self.m.Obj(-self.target)        
        
        
        
        try:
            self.m.solve(disp=False)
        except:
            print('EXCEPTION CAUGHT IN 2ND LAYER')
            self.errorFlag = True
        print('Sink X: {0}'.format(self.snkPos[0].value))
        print('Sink Y: {0}'.format(self.snkPos[1].value))
        print('Number of rounds for optimal amount of data sent: {0}'.format(self.rnds.value))
        self.expLifetime = self.rnds.value
        ################################################################
        #   This part executes the control input on the nodes and sink #
        if self.errorFlag:
            for CH in self.CHds:
                CH.setDesData(1)
                i+=1
            optimalP = [50, 50]
        else:
            i = 0
            for CH in self.CHds:
                CH.setDesData((self.dtrLst[i][0]))
                i+=1
            optimalP = [int(self.snkPos[0][0]), int(self.snkPos[1][0])]
                
        rmtree(self.m._path)
        
        return optimalP
    
    def refreshSolvers(self):
        self.resetGEKKO()
        self.errorFlag = False
        self.sink.resetGEKKO()
        #for node in self.nodes:
        #    node.resetGEKKO()
    
    
    def resetGEKKO(self):
        self.errorFlag = False
        self.m = GEKKO(remote = False)
        # time points

        self.CHxPos = []                                 # List of CH x/y positions as a Param()
        self.CHyPos = []
        self.CHdstLst = []
        
        self.nonCHxPos = []
        self.nonCHyPos = []
        self.nonCHdstLst = []
        
        self.e1Sum = []
        self.e2Sum = []

        self.dtrLst = []
        self.ECH_sum = []
        self.EnonCH_sum = []
        
        self.freeNonCHds = []
        # options
        self.m.options.IMODE = 3                 # optimize a solid state
        self.m.options.MAX_TIME = 10
    def plot(self):
        IDs = []
        for ch in self.CHds:
            IDs.append(str(ch.ID))


        ydtr = np.linspace(0,20,11)
        
        #maxDist = np.floor(np.sqrt(xSize**2 + ySize**2))
        maxDist = 150
        ydist = np.linspace(0, maxDist,16)
        
        CHDL = []
        for i in range(len(self.CHdstLst)):
            CHDL.append(self.CHdstLst[i][0])
        
        DTRL = []
        if(self.errorFlag):
            for chd in self.CHds:
                DTRL.append(chd.desData)
                
        else:
            for i in range(len(self.dtrLst)):  
                DTRL.append(self.dtrLst[i][0])
        
        plt.figure(self.nrplots)
        plt.subplot(2,1,1)
        plt.bar(IDs, CHDL, align='center', alpha=0.5)
        plt.yticks(ydist, ydist)
        plt.ylabel('distance')
        

        
        plt.subplot(2,1,2)
        plt.bar(IDs, DTRL, align='center', alpha=0.5)
        plt.yticks(ydtr, ydtr)
        plt.ylabel('Packets Desired')
        plt.xlabel('Node ID')
        plt.xticks(IDs, IDs)
        plt.show()
        
        plt.figure(self.nrplots+1)
        for ch in self.CHds:
            plt.plot(ch.xPos, ch.yPos, 'bo')  # plot x and y using blue circle markers
            pl.text(ch.xPos, ch.yPos, str(ch.ID), color="teal", fontsize=10)
        for nonch in self.nonCHds:
            plt.plot(nonch.xPos, nonch.yPos, 'go')  # plot x and y using blue circle markers
        plt.plot(self.snkPos[0].value, self.snkPos[1].value, 'ro', markersize=12)
    

if __name__ == "__main__":
    Hrz = 8
    Res = Hrz + 1
    
    testEnv = MPC2ndLayer(Hrz,Res)
    testEnv.cluster()
    print('Amount of Cluster Heads: {0}'.format(len(testEnv.CHds)))
    testEnv.controlEnv()
    for element in testEnv.CHds:
        print(element.desData)
    testEnv.plot()
    
    
    ch_dist = 0
    non_dist = 0

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            