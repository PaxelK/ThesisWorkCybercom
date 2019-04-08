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

nodeNr = 9                  #Choosing which node to do tests on

def iterateNodeFunc(node):
    EDA = 5*10**(-9)        # Data Aggregation Energy, units in Joules/bit
    Eamp = 100*10**(-12)    # Transmit Amplifier Types, units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)        
    Eelec = 50*10**(-9)     # Energy required to run circuity (both for transmitter and receiver), units in Joules/bit
    eBefore = node.getEnergy()
    packAmount = node.getPA()
    if(node.CHstatus == 0):
        packAmount = 1
    print('For node: ' + str(node.ID) + ', CH-status: ' + str(node.CHstatus))
    
    k = packAmount*node.pSize 
    dist = node.getDistance(node.CHparent)
    print('PA: ' + str(node.getPA()) + ', pSize: ' + str(node.pSize) + ', Dist: ' + str(dist) + ', Nr of Children: ' + str(node.conChildren))
    EC = ((Eelec+EDA)*node.pSize*node.conChildren + k*(Eelec + Eamp*dist**2))
    
    
    
    e = eBefore - EC
    tmp = 'Nrj before: ' + str(eBefore) + '\nNrj after: ' + str(e) + '\nNrj Consumed: ' + str(EC)
    print(tmp)
    
    return e





for i in range(10):
    #plotEnv(EE)
    
    #print(f"Round = {EE.rnd}")
    EE.updateEnv(1, 1, PRcontrl)
    EE.cluster()
    print('NEW CLUSTERING_____________')
    
    energyBefore = EE.nodes[nodeNr].getEnergy()
    nrjAfter = iterateNodeFunc(EE.nodes[nodeNr])
    diffIt = energyBefore - nrjAfter 
    
    
    EE.communicate()
    diffReal = energyBefore - EE.nodes[nodeNr].getEnergy()
    
    print(str(EE.nodes[nodeNr].conChildren))
    print('diff iter: ' + str(diffIt))
    print('Real diff: ' + str(diffReal))
    
    
    
    if(nrjAfter==EE.nodes[nodeNr].getEnergy()):
        print('YES!!')
    EE.iterateRound()
    
    







