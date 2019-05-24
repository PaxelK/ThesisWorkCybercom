# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:36:10 2019

@author: axkar1
"""

from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt


class MPC2ndLayer():
    def __init__(self):        
        self.verbose = False
        self.nrplots = 0
         
         
        self.m = GEKKO(remote=False)
        
        # constants
        self.Egen = 1*10**-5        # Amount of energy regenerated over a transmission round
        self.pSize = 1000           # Packet size
        #self.maxBattery = 1         # Maximum amount of "Joules" that a node can hold
        
        self.Eelec = 50*10**(-9)   	# Energy required to run circuity (both for transmitter and receiver), units in Joules/bit
        self.ETx = 50*10**(-9)     	# Units in Joules/bit
        self.ERx = 50*10**(-9)     	# Units in Joules/bit
        self.Eamp = 100*10**(-12)  	# Transmit Amplifier Types, units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
        self.EDA = 5*10**(-9)      	# Data Aggregation Energy, units in Joules/bit
        
        self.nds = 50                                   # ALL NODES
        self.PERC = 0.4                                 # Percentage of cluster heads
        self.CHs = int(self.nds*self.PERC)              # CLUSTER HEADS
        self.nonCHs = int(self.nds - self.CHs)          # NON-CHs
        self.CHLst = []                                 # List of CH positions Param()
        self.CHdistLst = []                             # List of CH distances to the receiving sink/base-station Var()
        #self.CHnrjLst = []                              # List of CH energy amount in battery
        
        self.nonCHLst = []                              # List of non-CH positions Param()
        self.nonCHdistLst = []                          # List of non-CHs distances Var()
        #self.nonCHnrjLst = []                           # List of nonCH energy amount in battery
        
        self.intermeds = []                             # List of intermediate equations for energy consumption of nodes

        #Counter for plots
        self.nrplots = 1;
    
        # options
        self.m.options.IMODE = 3                 # optimize a solid state

        
        
        

    def controlEnv(self):

        #WORKING SCRIPT FOR ONE DIMENSION
        
        self.sinkPos = self.m.Var(lb=0,ub=100)  # The sinks position as one of the controllable variables

        """
        Two for-loops creates and stores the position parameters and the distance variables
        of the cluster heads and the normal nodes in their respective arrays.
        """
        for i in range(self.CHs):
            self.CHLst.append(self.m.Param(value = 4*i))    # Multiplies with 4 just to spread them out along the line a bit sparser
            self.CHdistLst.append(self.m.Var(value = self.sinkPos.value - self.CHLst[i].value))
            self.m.Equation(self.CHdistLst[i] == self.sinkPos - self.CHLst[i])
        
        for i in range(self.nonCHs):
            self.nonCHLst.append(self.m.Param(value = 2*i)) # Multiplies with 2 just to spread them out along the line a bit sparser
            self.nonCHdistLst.append(self.m.Var(value = self.sinkPos.value - self.nonCHLst[i].value)) 
            
            self.m.Equation(self.nonCHdistLst[i] == self.sinkPos - self.nonCHLst[i])

        self.packs = 1                  # A constant value for number of nodes which a cluster head is receiving from while it is also transmitting. Set to 1 for simplicity
        self.dtrLst = []                # List containing all m.Vars deciding how many packets each cluster head ought to transmitt for maximum data received by the sink
        self.rnds = self.m.Var(integer = True, lb = 1)  # Variable for amount of transmission rounds of the system
        self.E_tot = self.m.Param(value = 3)    # Simplified parameter for the total energy of the system
        self.e1Sum = []     # Array containing all the intermediates describing the energy consumption of each CH
        self.e2Sum = []     # Array containing all the intermediates describing the energy consumption of each non-CH
        
        for i in range(self.CHs):
            self.dtrLst.append(self.m.Var(lb = 1, ub = 20))     # Adds the MV deciding the  amount of data packets transmitted by a CH 
            """
            The following intermediates describe the energy consumption of a CH (former)
            or a nonCH (latter). In rought terms it contains the energy loss of receiving signals as well as 
            transmitting signals: e = Erx + Etx
            The constants Eelec, EDA and Eamp are constants related to electrical circuit
            expenses
            """
            self.e1Sum.append(self.m.Intermediate((self.Eelec+self.EDA)*self.packs + self.dtrLst[-1]*self.pSize*(self.Eelec + self.Eamp * self.CHdistLst[i]**2)))            

        for i in range(self.nonCHs):
            self.e2Sum.append(self.m.Intermediate(self.packs*self.pSize*(self.Eelec + self.Eamp * self.nonCHdistLst[i]**2)))

        
        # Constraint saying that the total energy expenses of all nodes multiplied with the number 
        # of transmission rounds must be lesser than the total energy that reside in the network
        self.m.Equation(self.E_tot >= (self.m.sum(self.e1Sum)+ self.m.sum(self.e2Sum))*self.rnds)
        
        # The objective is set to maximize the amount of packages sent over all of rounds
        self.target = self.m.Intermediate(self.m.sum(self.dtrLst))
        self.m.Obj(-self.target*self.rnds)

        
        self.m.solve(disp=False)
        print('Sink\'s optimal Position: {0}'.format(self.sinkPos.value))
        print('Number of rounds for optimal amount of data transmitted: {0}'.format(self.rnds.value))




        
        
    def plot(self):
        objects = np.linspace(1,len(self.CHLst),len(self.CHLst))
            
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
        plt.ylabel('Distance')
        
        
        plt.subplot(2,1,2)
        plt.bar(y_pos, DTRL, align='center', alpha=0.5)
        plt.yticks(ydtr, ydtr)
        plt.ylabel('Packets Desired')
        plt.xlabel('Node#')
        
        plt.show()


if __name__ == "__main__":
    testEnv = MPC2ndLayer() 
    testEnv.controlEnv()
    testEnv.plot()
    