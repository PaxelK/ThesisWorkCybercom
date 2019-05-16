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
        self.Egen = 1*10**-3
        self.const = 0.6
        self.E = 1
        
        #Counter for plots
        self.nrplots = 1;
        
        #Threshold for when objective is seen as 0
        self.limit = np.float64(1e-10)
        
        self.resetGEKKO()
        
    def resetGEKKO(self):
        self.m = GEKKO(remote=False)
        self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        
        self.vp = np.zeros(self.ctrlRes)
        self.v = self.m.Param(value=self.vp)
        
        # define distance

        self.dist = self.m.Var()

        self.dtr = self.m.MV(value=1, integer = True, lb=0,ub=20)
        self.dtr.STATUS = 1
        
        # define energy level
        self.nrj_stored = self.m.Var(value = self.energy, lb = 0)
        
        self.data = self.m.Var()
          
        # energy to transmit
        self.e = self.m.Intermediate(((Eelec+EDA)*self.conChildren + self.dtr*self.pSize*(Eelec + Eamp * self.dist**2)) - self.Egen)
        
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
        self.final.value[int(np.floor(self.ctrlRes/2)):-1] = 0.001
        self.final.value[-1] = 1
        #self.m.Equation(self.final*(self.data)<=0)
        
        #self.m.Obj(self.data*self.final)
        
        self.target = self.m.Intermediate(self.m.sqrt((self.data*self.final)**2))
        self.m.Obj(self.target) # transmit data by the end
        
        
        
        # hard constraint
        # this form may cause infeasibility if it can't achieve
        # data=0 at the end
        #self.m.fix(self.data,self.ctrlRes-1,0)
        # options
        self.m.options.IMODE = 6                # optimal control
        self.m.options.NODES = 3                # collocation nodes
        self.m.options.SOLVER = 1               # solver (IPOPT), 1 is for when integers is used as MV
        self.m.options.TIME_SHIFT = 1           # Setting for saving values from last solve()
    
    def produce_vVector(self, xVec, yVec):
        vVec = np.zeros(len(xVec))
        for i in range(len(xVec)-1):
            dist_Before = np.float64(np.sqrt((xVec[i]-self.xPos)**2 + (yVec[i]-self.yPos)**2))   
            dist_After = np.float64(np.sqrt((xVec[i+1]-self.xPos)**2 + (yVec[i+1]-self.yPos)**2))       
            vVec[i] = np.float64((dist_After - dist_Before)/(self.ctrlHrz/(self.ctrlRes-1)))  
        return vVec
    
    def setDesData(self, dat):
        if(type(self.data.value.value) is list):
            self.data.value[0] = dat
        else:
            self.data.value = dat
        
    def controlPR(self, velocity):  
        tempVel = np.float64(velocity)
        tempNrj = np.float64(self.energy)
        tempDist = np.float64(self.getDistance(self.CHparent))
        
        
        self.vp[0:] = self.v.value[1]
        if(tempVel == self.vp[0]):
            if self.verbose:
                print('Velocity: {0} was equal to vVal0: {1}'.format(tempVel, self.vp[0]))
                print('Therefore, velocity was set as vp[1:]')
        else:
            if self.verbose:
                print('Velocity: {0} was not equal to vVal0: {1}'.format(tempVel, self.v.value[0]))
                print('Therefore, vp[1:] was set as tempVel = {0}'.format(tempVel))
            self.vp[1:] = tempVel         
        self.v.value = self.vp
        
        
        if(type(self.data.value.value) is list):
            if(self.data.value.value[0] <= self.limit):
                self.datap = np.zeros(self.ctrlRes)
                self.data.value[0] = 0
        
        #SETTING THE CURRENT ENERGY LEVEL
        if(type(self.nrj_stored.value.value) is list):
            #print('NRJ STORED WAS NOT FLOAT. IT WAS: {0}'.format(type(self.nrj_stored.value.value)))
            self.nrj_stored.value[0] = tempNrj
        else:
            self.nrj_stored.value = tempNrj
        
        # define distance
        if(type(self.dist.value.value) is list):
            #print('DIST WAS NOT INT, IT WAS: {0}'.format(type(self.dist.value.value)))
            self.dist.value[0] = tempDist
        else:
            self.dist.value = tempDist
        
        
        #if(self.data.value[0] <= limit):
        #    self.data.value[0] = 0
            #print(np.shape(testNode.vp))  
        if(type(self.dtr.value.value) is list):
            self.dtrp = np.zeros(self.ctrlRes)
            self.dtrp[0] = self.dtr.value[1]
            self.dtr.value = self.dtrp
            
            
            #self.nrj_stored.value[0] = self.nrj_stored.value[1]
            #self.data.value[0] = self.data.value[1]
        
        """
        self.dtrp = np.zeros(self.ctrlRes)
        self.dtrp[0] = self.dtr.value[1]
        self.dtr.value = self.dtrp
        
        self.nrj_storedp = np.zeros(self.ctrlRes)
        self.nrj_storedp[0] = self.nrj_stored.value[1]
        self.nrj_stored.value = self.nrj_storedp
        
        self.datap = np.zeros(self.ctrlRes)
        self.datap[0] = self.data.value[1]
        self.data.value = self.datap
        self.m.TIME_SHIFT = 1
        """
        #self.data.value[0] = self.data.value[1]
        self.m.solve(disp=False) # solve optimization problem
        self.setPR(self.dtr.value[0])
    
    
    def controlPR1(self, sink): 
        lel = self.produce_vVector(sink.xP.value, sink.yP.value)
        print('LELELELELEL')
        print(type(lel))
        self.v.value = self.produce_vVector(sink.xP.value, sink.yP.value)
        
        tempNrj = np.float64(self.energy)
        tempDist = np.float64(self.getDistance(self.CHparent))     
        
        if(type(self.data.value.value) is list):
            if(self.data.value.value[0] <= self.limit):
                self.data.value[0] = 0
        
        #SETTING THE CURRENT ENERGY LEVEL
        if(type(self.nrj_stored.value.value) is list):
            #print('NRJ STORED WAS NOT FLOAT. IT WAS: {0}'.format(type(self.nrj_stored.value.value)))
            self.nrj_stored.value[0] = tempNrj
        else:
            self.nrj_stored.value = tempNrj
        
        # define distance
        if(type(self.dist.value.value) is list):
            #print('DIST WAS NOT INT, IT WAS: {0}'.format(type(self.dist.value.value)))
            self.dist.value[0] = tempDist
        else:
            self.dist.value = tempDist
        
        
        #if(self.data.value[0] <= limit):
        #    self.data.value[0] = 0
            #print(np.shape(testNode.vp))  
        if(type(self.dtr.value.value) is list):
            self.dtrp = np.zeros(self.ctrlRes)
            self.dtrp[0] = self.dtr.value[1]
            self.dtr.value = self.dtrp
            
            
            #self.nrj_stored.value[0] = self.nrj_stored.value[1]
            #self.data.value[0] = self.data.value[1]
        
        """
        self.dtrp = np.zeros(self.ctrlRes)
        self.dtrp[0] = self.dtr.value[1]
        self.dtr.value = self.dtrp
        
        self.nrj_storedp = np.zeros(self.ctrlRes)
        self.nrj_storedp[0] = self.nrj_stored.value[1]
        self.nrj_stored.value = self.nrj_storedp
        
        self.datap = np.zeros(self.ctrlRes)
        self.datap[0] = self.data.value[1]
        self.data.value = self.datap
        self.m.TIME_SHIFT = 1
        """
        #self.data.value[0] = self.data.value[1]
        self.m.solve(disp=False) # solve optimization problem
        self.setPR(self.dtr.value[0])
    
    
    
    def plot(self):
        plt.figure(self.nrplots)
        plt.subplot(6,1,1)
        plt.plot(self.m.time,self.dist.value,'r-',label='Distance')
        plt.legend()
        
        plt.subplot(6,1,2)
        #plt.plot(self.m.time,self.v.value,'k--',label='Velocity')
        plt.step(self.m.time,self.v.value,'k--',label='Velocity')
        plt.legend()
        
        plt.subplot(6,1,3)
        plt.plot(self.m.time,self.e.value,'b-',label='Energy Consumption')
        plt.legend()
        
        plt.subplot(6,1,4)
        plt.plot(self.m.time, self.data.value,'k.-',label='Data Remaining')
        #plt.bar(self.m.time, self.data.value, align='center', alpha=0.5)
        plt.legend()
        
        
        plt.subplot(6,1,5)
        #plt.plot(self.m.time, self.dtr.value,'r-',label='Transmission Rate')
        plt.step(self.m.time, self.dtr.value,'r-',label='Transmission Rate')
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
    
    
        
    def clearGEKKO(self):
        self.m.clear()


if __name__ == "__main__":
    Hrz = 4
    Res = Hrz + 1
    
    testNode = MPCnode(1,20,20,0.05,Hrz,Res)
    testNode.CHstatus = 1
    
    testNode1 = MPCnode(2,20,60,0.05,Hrz,Res)
    testNode1.CHstatus = 1
    
    testNode2 = Sink(100, 100)
    
    testNode.connect(testNode2)
    testNode1.connect(testNode2)
    #print('x: {0}, y: {1}'.format(testNode2.xPos,testNode2.yPos))
    testNode2.move(-30,-10)
    #print('x: {0}, y: {1}'.format(testNode2.xPos,testNode2.yPos))
    #print('Distance to sink: {0}'.format(testNode.getDistance(testNode2)))
    #print("Segment: {0}, PR: {1}, PS: {2}".format(0,testNode.PA, testNode.getPS()))
    #print(testNode.data.value)
    #testNode.sendMsg(testNode2)
    
    #testNode.plot()
    #testNode.controlPR(0,0)
    #testNode.m.time[Hrz-1] = testNode.m.time[Hrz]-0.0000000000001
    testNode.setDesData(100000)
    testNode1.setDesData(100000)
    for j in range(1):
        print('lel')
        if(j > 0):
            testNode.PS = 0
            testNode1.PS = 0
            testNode.resetGEKKO()
            testNode1.resetGEKKO()
        for i in range(10):
            testNode.updateEnergy(-testNode.Egen)
            testNode1.updateEnergy(-testNode1.Egen)
            """        
            if(i == 5):
                testNode.setDesData(50000)
                testNode1.setDesData(50000)
                """    
            if(i<=int(np.floor(Hrz/2))):
                testNode.controlPR(-5)
                testNode.sendMsg(testNode2)
                
                testNode1.controlPR(5)
                testNode1.sendMsg(testNode2)
                
                testNode2.move(0,-5)
            else:
                testNode.controlPR(0)
                testNode.sendMsg(testNode2)
                
                testNode1.controlPR(0)
                testNode1.sendMsg(testNode2)
            testNode.plot()
            #testNode.controlPR(0)
            #testNode.sendMsg(testNode2)    
            
            print("Segment: {0} | Node | PR  | PS\t\t|\n\t\t {1}   {2}   {3} \n\t\t {4}   {5}   {6}".format(i, testNode.ID, testNode.dtr.value[0], testNode.getPS(), testNode1.ID, testNode1.dtr.value[0], testNode1.getPS()))
            print("Node {0} Data:\n{1}\nNode {2} Data:\n{3}".format(testNode.ID, testNode.data.value, testNode1.ID, testNode1.data.value))
            
     
        
        
          
    print(testNode2.getDataRec())
        
        
        
        
        
        
        