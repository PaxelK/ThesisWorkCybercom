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
from MPCsink import MPCsink
from setParamsMPC import *
from collections import OrderedDict
import random as rand


class MPCnode(Node):
    def __init__(self, id, x, y, nrj, ctrlHrz, ctrlRes):
        super().__init__(id, x, y, nrj)  
        
        self.verbose = False
        self.errorFlag = False
        
        # Creates the optimizing GEKKO module 
        self.m = GEKKO(remote=False)
        
        # Horizon, time points
        self.ctrlHrz = ctrlHrz                  # Control Horizon
        self.ctrlRes = ctrlRes                  # Control Resolution. Number of control steps within the control horizon
        self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        self.desData = 0
        self.DLcounter = 0                      # Counts control steps during a round in order to be able to move the deadline forward after each control cycle
        # constants
        self.Egen = 1*10**-5
        self.Egen = 0
        
        # Counter for plots, list for plot colors to choose from
        self.nrplots = 1;
        self.pltColors = ['r-', 'k-', 'b-', 'g-', 'y-', 'c-', 'm-']
        self.labels = ["Distance", "Velocity","Energy Consumption", "Data Remaining", "Transmission Rate", "Battery"]
        colorNr = rand.randrange(0, len(self.pltColors),1)
        self.lineColor = self.pltColors[colorNr]

        # Resets the gekko module so that the optimizing can be done with new parameters and variables
        self.resetGEKKO()
        
    def resetGEKKO(self):
        self.errorFlag = False          # Sets errorflag back to false
        self.m = GEKKO(remote=False)    # Creates new GEKKO module
        self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        
        self.vp = np.zeros(self.ctrlRes)
        self.v = self.m.Param(value=self.vp)
        
        # define distance
        self.dist = self.m.Var()

        self.dtr = self.m.MV(value=0, integer = True, lb=0,ub=20)
        self.dtr.STATUS = 1
        # define energy level
        self.nrj_stored = self.m.Var(value = self.energy, lb = 0)
        
        self.data = self.m.Var(value = self.desData)
        self.DSround = 0        # Data sent this round
        
        
        self.e = self.m.Intermediate(((Eelec+EDA)*self.conChildren + self.dtr*self.pSize*(Eelec + Eamp * self.dist**2)) - self.Egen)
        
        # equations
        # track the position
        self.m.Equation(self.dist.dt() == self.v)
        self.m.Equation(self.nrj_stored.dt() == -self.e)
        self.m.Equation(self.nrj_stored >= self.e)
        # as data is transmitted, remaining data stored decreases
        self.m.Equation(self.data.dt() == -self.dtr*self.pSize)
        
        self.deadline = self.m.Var(value=self.ctrlHrz)
        self.dlCost = self.m.Var()
        self.m.Equation(self.deadline.dt() == -1)
        # self.m.Equation(self.energy >= self.e)
        
        # objective
        
        #self.data.SP = 0
        
        # soft (objective constraint)
        self.final = self.m.Param(value=np.zeros(self.ctrlRes))
        self.final.value[-1] = 1
        
        
        self.target = self.m.Intermediate((self.final*(0-self.data)**2))
        self.m.Obj(self.target) # transmit data by the end
        self.m.Obj(self.e)
        #self.m.Obj(self.final*self.data)
        
        # options
        # Solutions forced to terminate early by the MAX_TIME constraint do 
        # not satisfy the Karush Kuhn Tucker conditions for optimality.
        self.m.options.MAX_TIME = 10 
        self.m.options.IMODE = 6                # optimal control
        self.m.options.NODES = 3                # collocation nodes
        #self.m.options.CTRLMODE = 3
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
        self.desData = dat*self.pSize
        #if(type(self.data.value.value) is list):
        #    self.data.value[0] = dat*self.pSize
        #else:
        #    self.data.value = dat*self.pSize
            
    def plot(self, **kwargs):
        plt.figure(self.nrplots)
        plt.subplot(6,1,1)
        dist_line = plt.plot(self.m.time[1:],self.dist.value[1:],self.lineColor,label=self.labels[0])
        distance_legend = plt.legend(handles=dist_line )
            
        plt.subplot(6,1,2)
        #plt.plot(self.m.time,self.v.value,self.lineColor,label=self.labels[1])
        vel_line = plt.step(self.m.time[1:],self.v.value[1:], self.lineColor,label=self.labels[1], where = 'post')
        vel_legend = plt.legend(handles=vel_line)
            
        plt.subplot(6,1,3)
        #plt.plot(self.m.time,self.e.value,self.lineColor,label=self.labels[2])
        energyCons_line = plt.step(self.m.time[1:],self.e.value[1:],self.lineColor,label=self.labels[2], where = 'post')
        nrjcons_legend = plt.legend(handles=energyCons_line)
            
            
        plt.subplot(6,1,4)
        dataRem_line = plt.plot(self.m.time[1:], self.data.value[1:],self.lineColor,label=self.labels[3])
        #plt.bar(self.m.time, self.data.value, align='center', alpha=0.5)
        dataRem_legend = plt.legend(handles=dataRem_line)
        
            
        plt.subplot(6,1,5)
        #plt.plot(self.m.time, self.dtr.value,'r-',label='Transmission Rate')
        transmRate_line = plt.step(self.m.time[1:], self.dtr.value[1:],self.lineColor,label=self.labels[4], where = 'post')
        tr_legend = plt.legend(handles=transmRate_line)
            
        plt.subplot(6,1,6)
        battery_line = plt.plot(self.m.time[1:],self.nrj_stored[1:],self.lineColor,label=self.labels[5])
        battery_legend = plt.legend(handles=battery_line)
        
        if('timesegment' in kwargs):
            plt.xlabel('Time, Segm {0}'.format(kwargs['timesegment']))
        else:
            plt.xlabel('Time')
            
        #plt.show()
            
        self.nrplots+=1


    def controlPR(self, sink): 
        #print('ELELELELE')
        #print(self.desData)
        #print(self.data.value)
        self.resetGEKKO()
        #self.data.value = self.desData
        #print('ELELELELE SECOND TIME')
        #print(self.desData)
        #print(self.data.value)
        
        
        self.v.value = self.produce_vVector(sink.xP.value, sink.yP.value)
        
        tempNrj = np.float64(self.energy)
        tempDist = np.float64(np.abs(self.getDistance(self.CHparent)))  
        
        #SETTING THE CURRENT ENERGY LEVEL
        if(type(self.nrj_stored.value.value) is list):
            self.nrj_stored.value[0] = tempNrj
        else:
            self.nrj_stored.value = tempNrj
        
        # define distance
        if(type(self.dist.value.value) is list):
            self.dist.value[0] = tempDist
        else:
            self.dist.value = tempDist
        
        #if(type(self.dtr.value.value) is list):
        #    print('dtr.value BEFORE: {0}'.format(self.dtr.value))
        #    self.dtr.value = self.dtr.value[1]
        #    print('dtr.value AFTER: {0}'.format(self.dtr.value))
        
        """
        In order to move the horizon forward to make sure that the deadline is held 
        (finish transmitting it's desired data before the time segments run out),
        the following if-block checks if the difference between total time segments
        and past time segments is equal or smaller than the controller's horizon.
        
        If it is, it is time to start rolling the end-value point forward. 
        The objective function prioritizes solutions that reaches the desired state in  
        steps before final[wherever the 1-value is].
        """
        if((time_segments-self.DLcounter)<=self.ctrlHrz):
            self.final.value = np.roll(self.final.value, -((self.ctrlHrz)-(time_segments-self.DLcounter)))
        
        try:
            self.m.solve(disp=False)
            self.PA = self.dtr.value[1]
            self.desData -= self.dtr.value.value[1]*self.pSize
            self.DLcounter += 1
        except:
            print('EXCEPTION CAUGHT FOR NODE {0}'.format(self.ID))
            self.setPR(0)
            self.errorFlag = True
            self.DLcounter += 1
        
        if(self.DLcounter > time_segments):
            self.DLcounter = 0












if __name__ == "__main__":
    Hrz = 10
    Res = Hrz + 1
    
    testNode = MPCnode(1,20,20,0.05,Hrz,Res)
    testNode.CHstatus = 1
    
    testNode1 = MPCnode(2,20,60,0.05,Hrz,Res)
    testNode1.CHstatus = 1
    
    sink = MPCsink(100, 100, Hrz, Res)
    
    testNode.connect(sink)
    testNode1.connect(sink) 
    
    sink.setTarPoint(30, 30)


    testNode.setDesData(1)
    testNode1.setDesData(70)
    testNode.energy = 0.005
    testNode1.energy = 0.05
    for j in range(1):
        if(j > 0):
            testNode.PS = 0
            testNode1.PS = 0
            testNode.resetGEKKO()
            testNode1.resetGEKKO()
        for i in range(10):
            testNode.updateEnergy(-testNode.Egen)
            testNode1.updateEnergy(-testNode1.Egen)
            sink.produce_MoveVector()
            
            testNode.controlPR(sink)
            testNode.sendMsg(sink)
            
            testNode1.controlPR(sink)
            testNode1.sendMsg(sink)
            
            
            sink.move(sink.xMove.value[1], sink.yMove.value[1])
            testNode1.plot(timesegment = i)
 
            print("Segment: {0} | Node | PR  | PS\t\t|\n\t\t {1}   {2}   {3} \n\t\t {4}   {5}   {6}".format(i, testNode.ID, testNode.getPA(), testNode.getPS(), testNode1.ID, testNode1.getPA(), testNode1.getPS()))
            print("Node {0}:\n Data: {1}\nPR: {4}\nFinal: {6}\n\nNode {2}\n Data: {3}\nPR: {5}\nFinal: {7}".format(testNode.ID, testNode.data.value, testNode1.ID, testNode1.data.value, testNode.dtr.value, testNode1.dtr.value,testNode.final.value, testNode1.final.value))
            print('\n')
                
          
    print(sink.getDataRec())
        