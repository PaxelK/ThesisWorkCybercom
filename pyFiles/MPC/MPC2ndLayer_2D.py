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
        self.CHxPos = []                                 # List of CH x/y positions as a Param()
        self.CHyPos = []
        self.CHdstLst = []
        
        self.nonCHxPos = []
        self.nonCHyPos = []
        self.nonCHdstLst = []
        
        #Counter for plots
        self.nrplots = 1;
    
        
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
        
        if self.verbose:
            print('CHxPos:\n {0}'.format(self.CHxPos))
            print('CHyPos:\n {0}'.format(self.CHyPos))
            print('CHdstLst:\n {0}'.format(self.CHdstLst))
        
        for i in range(len(self.nonCHds)):
            self.nonCHxPos.append(self.m.Param(value = self.nonCHds[i].xPos))
            self.nonCHyPos.append(self.m.Param(value = self.nonCHds[i].yPos))
            
            temp = np.sqrt((self.nonCHds[i].xPos)**2 + (self.nonCHds[i].yPos)**2)
            
            self.nonCHdstLst.append(self.m.Var(value = temp))
            self.m.Equation(self.nonCHdstLst[i] == self.m.sqrt((self.snkPos[0] - self.nonCHxPos[i])**2 + (self.snkPos[1] - self.nonCHyPos[i])**2))
        
        if self.verbose:
            print('nonCHxPos:\n {0}'.format(self.nonCHxPos))
            print('nonCHyPos:\n {0}'.format(self.nonCHyPos))
            print('nonCHdstLst:\n {0}'.format(self.nonCHdstLst))
        
        self.dtrLst = []
        self.rnds = self.m.Var(integer = True, lb = 0)
        self.ECH_sum = []
        self.EnonCH_sum = []
        
        for i in range(len(self.CHds)):
            self.ECH_sum.append(self.m.Var(value = self.CHds[i].energy))
        for i in range(len(self.nonCHds)):
            self.EnonCH_sum.append(self.m.Var(value = self.nonCHds[i].energy))
        
        if self.verbose:
            print('ECH_sum:\n {0}'.format(self.ECH_sum))
            print('ECH_sum:\n {0}'.format(self.m.sum(self.ECH_sum).value))
            print('EnonCH_sum:\n {0}'.format(self.EnonCH_sum))


        self.E_total = self.m.Intermediate(self.m.sum(self.ECH_sum) + self.m.sum(self.EnonCH_sum))
        
        E_temp = 0
        for node in self.nodes:
            E_temp += node.energy
        self.E_tot = self.m.Param(value = E_temp)
        self.e1Sum = []
        self.e2Sum = []
        
        
        for i in range(len(self.CHds)):
            self.dtrLst.append(self.m.Var(lb = 1, ub = 20))
            self.e1Sum.append(self.m.Intermediate((Eelec+EDA)*self.CHds[i].conChildren + self.dtrLst[-1]*self.pSize*(Eelec + Eamp * self.CHdstLst[i]**2)))
            self.m.Equation(self.ECH_sum[i] >= self.e1Sum[i])

        for i in range(len(self.nonCHds)):
            self.e2Sum.append(self.m.Intermediate(self.nonCHds[i].PA*self.pSize*(Eelec + Eamp * self.nonCHdstLst[i]**2)))
            self.m.Equation(self.EnonCH_sum[i] >= self.e2Sum[i])
            
        if self.verbose:
            print('dtrLst:\n {0}'.format(self.dtrLst))
            print('e1Sum:\n {0}'.format(self.e1Sum))
            print('e2Sum:\n {0}'.format(self.e2Sum))
            print('E_tot:\n {0}'.format(self.E_tot.value))
            
        self.m.Equation(self.E_tot >= (self.m.sum(self.e1Sum)+ self.m.sum(self.e2Sum))*self.rnds)
        #self.m.Equation(self.E_total >= (self.m.sum(self.e1Sum)+ self.m.sum(self.e2Sum))*self.rnds)
        
        
        self.target = self.m.Intermediate(self.m.sum(self.dtrLst)*(self.rnds-1))
        self.m.Obj(-self.target)        
        
        self.m.solve(disp=False)
        print('Sink X: {0}'.format(self.snkPos[0].value))
        print('Sink Y: {0}'.format(self.snkPos[1].value))
        print('Number of rounds for optimal amount of data sent: {0}'.format(self.rnds.value))
    
    def resetGEKKO(self):
        self.m = GEKKO(remote = False)
    
    """
    def largest_prime_factor(self, n):
        i = 2
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
        return n    
    
    def prime_factors(self, n):
        i = 2
        factors = []
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                factors.append(i)
        if n > 1:
            factors.append(n)
        return factors
    """    
    def plot(self):
        objects = np.linspace(0,len(self.CHdstLst)-1,len(self.CHdstLst))
        objects1 = []
        for ch in self.CHds:
            objects1.append(ch.ID)
        objectNames = []
        for objID in objects1:
            print(objID)
            objectNames.append(str(objID))
        
        y_pos = np.arange(len(objects))
        
        #y_pos1 = np.arange(len(objects1))
        
        ydtr = np.linspace(0,20,11)
        
        #maxDist = np.floor(np.sqrt(xSize**2 + ySize**2))
        maxDist = 150
        ydist = np.linspace(0, maxDist,16)
        
        CHDL = []
        for i in range(len(self.CHdstLst)):
            CHDL.append(self.CHdstLst[i][0])
        
        DTRL = []
        for i in range(len(self.dtrLst)):
            DTRL.append(self.dtrLst[i][0])
        
        plt.figure(self.nrplots)
        plt.subplot(2,1,1)
        plt.bar(objectNames, CHDL, align='center', alpha=0.5)
        plt.yticks(ydist, ydist)
        plt.ylabel('distance')
        
        #plt.xticks(objectNames, objectNames)
        
        plt.subplot(2,1,2)
        plt.bar(objectNames, DTRL, align='center', alpha=0.5)
        plt.yticks(ydtr, ydtr)
        plt.ylabel('Packets Desired')
        plt.xlabel('Node ID')
        plt.xticks(objectNames, objectNames)
        plt.show()
        
        plt.figure(self.nrplots+1)
        for ch in self.CHds:
            plt.plot(ch.xPos, ch.yPos, 'bo')  # plot x and y using blue circle markers
            pl.text(ch.xPos, ch.yPos, str(ch.ID), color="teal", fontsize=10)
        for nonch in self.nonCHds:
            plt.plot(nonch.xPos, nonch.yPos, 'go')  # plot x and y using blue circle markers
        plt.plot(self.snkPos[0].value, self.snkPos[1].value, 'ro', markersize=12)
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
    