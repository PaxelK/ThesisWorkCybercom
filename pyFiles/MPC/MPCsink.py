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

class MPCsink(Sink):
    def __init__(self, sizex, sizey, ctrlHrz, ctrlRes):
        super().__init__(sizex, sizey)  
        self.ctrlHrz = ctrlHrz
        self.ctrlRes = ctrlRes
        self.v = 1
        
        #Counter for plots
        self.nrplots = 1;
        
        self.resetGEKKO()
        
        
        
        
    def resetGEKKO(self):
        self.m = GEKKO(remote = False)
        self.m.time = np.linspace( 0, self.ctrlHrz, self.ctrlRes)
        self.m.TIME_SHIFT = 1
        
        
        self.xMove = self.m.MV(integer = True, lb=-self.v,ub=self.v)
        self.xMove.STATUS = 1
        self.yMove = self.m.MV(integer = True, lb=-self.v,ub=self.v)
        self.yMove.STATUS = 1
        
        
        self.xP = self.m.Var(value = self.xPos, lb = 0, ub= 100)
        self.yP = self.m.Var(value = self.yPos, lb = 0, ub= 100)
        
        self.xTar = self.m.Param()
        self.yTar = self.m.Param()
        
        self.xDist = self.m.CV()
        self.xDist.STATUS = 1
        self.yDist = self.m.CV()
        self.yDist.STATUS = 1
        self.m.options.CV_TYPE = 2                          #Squared Error
        self.m.Equation(self.xDist == self.xP - self.xTar)
        self.m.Equation(self.yDist == self.yP - self.yTar)
        
        self.m.Equation(self.xDist.dt() == self.xMove)
        self.m.Equation(self.yDist.dt() == self.yMove)
        
        self.xErr = self.m.Intermediate((self.xTar - self.xP))
        self.yErr = self.m.Intermediate((self.yTar - self.yP))
        
        
        self.xDist.SP = 0
        self.yDist.SP = 0
        
        self.m.options.IMODE = 6 
    
    def setTarPoint(self, x, y):
        self.xTar.value = x
        self.yTar.value = y
        
        
    def produce_MoveVector(self):
        if(type(self.xDist.value.value) is not list):
            self.xDist.value = self.xP.value - self.xTar.value
            self.yDist.value = self.yP.value - self.yTar.value 
        else:
            self.xMove[0] = self.xMove.NXTVAL
            self.yMove[0] = self.yMove.NXTVAL
            self.xP[0] = self.xPos
            self.yP[0] = self.yPos
            
            if(type(self.xTar.value.value) is list):
                self.xTar.value = self.xTar.value.value[0]
                self.yTar.value = self.yTar.value.value[0]
                self.xDist.value = self.xP.value[0] - self.xTar.value.value
                self.yDist.value = self.yP.value[0] - self.yTar.value.value
            else:
                self.xDist.value[0] = self.xP.value[0] - self.xTar.value.value
                self.yDist.value[0] = self.yP.value[0] - self.yTar.value.value
                
        #print('xTar: {0}\n yTar: {1}\n xDst: {2}\n yDst: {3}\n'.format(self.xTar.value,self.yTar.value,self.xDist.value,self.yDist.value))
        self.m.solve(disp = False)
        #print('SECOND PRINT')
        #print('xTar: {0}\n yTar: {1}\n xDst: {2}\n yDst: {3}\n'.format(self.xTar.value,self.yTar.value,self.xDist.value,self.yDist.value))

        
        
    def plot(self):
        plt.figure(self.nrplots)
        plt.subplot(4,1,1)
        plt.step(self.m.time,self.xDist,'r-',label='X-DIST')
        plt.legend()
        
        plt.subplot(4,1,2)
        plt.step(self.m.time,self.xMove,'b-',label='X-VEL')
        plt.legend()
        
        plt.subplot(4,1,3)
        #plt.plot(self.m.time,self.v.value,'k--',label='Velocity')
        plt.step(self.m.time,self.yDist,'k--',label='Y-DIST')
        plt.legend()
        
        plt.subplot(4,1,4)
        plt.step(self.m.time,self.yMove,'b-',label='Y-VEL')
        plt.legend()
        
        self.nrplots += 1







if __name__ == "__main__":
    testSink = MPCsink(100, 100, 10,11)
    #testSink.produce_MoveVector(59,46)
    #testSink.plot()
    
    for i in range(2):
        testSink.setTarPoint(59,46)
        testSink.produce_MoveVector()
        #print('xPos: {0} \n xVel: {1}'.format(testSink.xDist.value, testSink.xMove.value))
        testSink.move(testSink.xMove.value[1], testSink.yMove.value[1])
        testSink.plot()
        
        
    