# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:25:41 2019

@author: axkar1
"""
from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from Node import Node
from Sink import Sink
from setParams import *

class MPCnode(Node):
    def __init__(self, id, x, y, nrj, ctrlHrz, ctrlRes):
        super().__init__(id, x, y, nrj)  
        
        self.verbose = False
        
        self.m = GEKKO(remote=False)
        # time points
        self.ctrlHrz = ctrlHrz                  # Control Horizon
        self.ctrlRes = ctrlRes                  # Control Resolution. Number of control steps within the control horizon
        self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        # constants
        self.Egen = 1*10**-5
        self.const = 0.6
        self.packet = 1
        self.E = 1
        
        
        self.nrplots = 1;
        
        # define velocity profile
        self.vp = np.zeros(self.ctrlRes)
        self.v = self.m.Param(value=self.vp)

        # define distance
        self.dist = self.m.Var(20)

        # define data transmission rate
        self.dtr = self.m.MV(value=self.PA, integer = True, lb=1,ub=20)
        self.dtr.STATUS = 1
        
        # define energy level
        self.nrj_stored = self.m.Var(value = self.energy, lb = 0)
        
        # define how much data must be transmitted
        amount = self.pSize*100 
        self.data = self.m.Var(value = amount, lb = 0)
        
        # energy to transmit
        self.e = self.m.Intermediate(((Eelec+EDA)*self.packet + self.dtr*self.pSize*(Eelec + Eamp * self.dist**2)) - self.Egen)
        # equations
        
        # track the position
        self.m.Equation(self.dist.dt() == self.v)
        self.m.Equation(self.nrj_stored.dt() == -self.e)
        # as data is transmitted, remaining data stored decreases
        self.m.Equation(self.data.dt() == -self.dtr*self.pSize)
        # self.m.Equation(self.energy >= self.e)
        
        # objective
        self.m.Obj(self.e) # minimize energy
        
        # soft (objective constraint)
        self.final = self.m.Param(value=np.zeros(self.ctrlRes))
        self.final.value[-1] = 1
        self.m.Obj(self.data*self.final) # transmit data by the end
        
        # hard constraint
        # this form may cause infeasibility if it can't achieve
        # data=0 at the end
        #self.m.fix(self.data,self.ctrlRes-1,0)
        # options
        self.m.options.IMODE = 6  # optimal control
        self.m.options.NODES = 3  # collocation nodes
        self.m.options.SOLVER = 1 # solver (IPOPT)
        self.m.solve(disp=False)
        
       
        
        
    def plot(self):
        plt.figure(self.nrplots)
        plt.subplot(6,1,1)
        plt.plot(self.m.time,self.dist.value,'r-',label='Distance')
        plt.legend()
        
        plt.subplot(6,1,2)
        plt.plot(self.m.time,self.v.value,'k--',label='Velocity')
        plt.legend()
        
        plt.subplot(6,1,3)
        plt.plot(self.m.time,self.e.value,'b-',label='Energy Consumption')
        plt.legend()
        
        plt.subplot(6,1,4)
        plt.plot(self.m.time, self.data.value,'k.-',label='Data Remaining')
        plt.legend()
        
        
        plt.subplot(6,1,5)
        plt.plot(self.m.time, self.dtr.value,'r-',label='Transmission Rate')
        plt.legend()
        
        plt.subplot(6,1,6)
        plt.plot(self.m.time,self.nrj_stored,'b-',label='Battery')
        plt.legend()
        plt.xlabel('Time')
        
        self.nrplots+=1

    def getDeltaDist(self, sinkX, sinkY, sdeltaX, sdeltaY, deltaDist):        
        distBefore = np.sqrt((sinkX**2)+(sinkY**2))
        distAfter = np.sqrt(((sinkX+sdeltaX)**2)+((sinkY+sdeltaY)**2))
        self.deltaDist = distAfter - distBefore
        return self.deltaDist
    
    def controlPR(self, velocity, timepoint):        
        # solve optimization problem
        self.vp = np.ones(self.ctrlRes)
        self.vp[timepoint:] = velocity
        self.v.value = self.vp
        #print(np.shape(testNode.vp))        
        

        self.m.solve(disp=False)

        self.setPR(self.dtr.value[timepoint+1])



if __name__ == "__main__":
    testNode = MPCnode(1,20,20,0.05,10,11)
    testNode.CHstatus = 1
    testNode2 = Sink(100, 100)
    testNode.connect(testNode2)
    print('x: {0}, y: {1}'.format(testNode2.xPos,testNode2.yPos))
    testNode2.move(-30,-10)
    print('x: {0}, y: {1}'.format(testNode2.xPos,testNode2.yPos))
    print('Distance to sink: {0}'.format(testNode.getDistance(testNode2)))
    
    
    testNode.plot()
    for i in range(10):
        if(i==1):
            testNode.sendMsg(testNode2)
        if((i>=2) & (i<6)):
            testNode2.move(0,10)
            testNode.controlPR(10,i)
            testNode.sendMsg(testNode2)
            
        if(i>=6):
            testNode2.move(0,-5)
            testNode.controlPR(-5,i)
            testNode.sendMsg(testNode2)
        testNode.plot()
        print("Segment: {0}, PR: {1}".format(i,testNode.PA))
        
        
        
        
        
        
        