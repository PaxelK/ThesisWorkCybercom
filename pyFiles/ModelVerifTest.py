# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:44:30 2019

@author: axkar1
"""

from EnvironmentEngine import *
from plotEnv import *

EE = EnvironmentEngine()  # Initiate environment

x, y = EE.sink.getPos()  # Get position/coordinates of sink

# Get PR for all nodes (PR should be zero for dead nodes)
PRcontrl = []
for i in range(numNodes):
    PRcontrl.append([i, 10])  # [Node ID, PR of node]

states = EE.getStates()


for i in range(10):
    plotEnv(EE)
    print(f"Round = {EE.rnd}")
    EE.updateEnv(1, 1, PRcontrl)
    EE.cluster()
    EE.communicate()
    EE.iterateRound()
    
    







def iterateNodeFunc(node):
    EDA = 5*10**(-9)      # Data Aggregation Energy, units in Joules/bit
    Eamp = 100*10**(-12)  # Transmit Amplifier Types, units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)        
    Eelec = 50*10**(-9)   # Energy required to run circuity (both for transmitter and receiver), units in Joules/bit
    
    e = node.getEnergy()
    
    nrj =  - ((Eelec+EDA)*packet + pr*PRmax*(Eelec + Eamp * d2)) 
                    