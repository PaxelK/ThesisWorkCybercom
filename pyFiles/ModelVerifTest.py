# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:44:30 2019

@author: axkar1
"""

from EnvironmentEngine import *
from plotEnv import *

EE = EnvironmentEngine()  # Initiate environment

# Get PR for all nodes (PR should be zero for dead nodes)
PRcontrl = []
for i in range(numNodes):
    PRcontrl.append([i, 1])  # [Node ID, PR of node]

states = EE.getStates()

nodeNr = 3                  #Choosing which node to do tests on

def iterateNodeFunc(node, env):
    '''
    Function that calculates how the energy and data aggregated changes in a node over one transmission round.
    
    INPUTS: 
        Node which values are to be observed. Environment containing total number of nodes and the sink.
        
    OUTPUTS:
        e - Predicted total energy still left in the node
        d - Predicted total data received by the node after communicate
        s - Predicted total data received by the sink after communicate
    '''
    verbose = False;                        #Variable to toggle tracing comments with. If false, they do not show.
    EDA = 5*10**(-9)                        # Data Aggregation Energy, units in Joules/bit
    Eamp = 100*10**(-12)                    # Transmit Amplifier Types, units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)        
    Eelec = 50*10**(-9)                     # Energy required to run circuity (both for transmitter and receiver), units in Joules/bit
    eBefore = node.getEnergy()              # Node's starting energy is sampled.
    dBefore = node.getDataRec()             # Node's starting bits received.
    sdBefore = env.sink.getDataRec()        # Sink start point bits received
    packAmount = node.getPA()               # Checks if CH or not and adjusts it's packet rate to 1 if not.
    if(node.CHstatus == 0):
        packAmount = 1
    
    k = packAmount*node.pSize               # Packet size to be transmitted
    dist = node.getDistance(node.CHparent)  # Distance to parent
    
    '''
    Energy consumed is formulated as:
        [nr of connected nodes]*ERx + ETx
        
    Data received for node is formulated as:
        [nr of connected nodes]*[standard packet size]
    '''
    EC = ((Eelec+EDA)*node.pSize*node.conChildren + k*(Eelec + Eamp*dist**2))
    datRec = node.pSize*node.conChildren
    etx  = k*(Eelec + Eamp*dist**2)
    if(node.conChildren != 0):
        erx = (Eelec+EDA)*node.pSize*node.conChildren/node.conChildren
    else:
        erx = 0
    
    '''
    Data received for sink is formulated as:
        [nr of nodes in network]*[standard size of package]
    This currently relies on the packet rate not changing between CHs and regular nodes
    '''
    snkDataRec = len(EE.nodesAlive)*node.pSize
    
    e = eBefore - EC
    d = dBefore + datRec
    s = sdBefore + snkDataRec
    if(verbose):
        print('For node: ' + str(node.ID) + ', CH-status: ' + str(node.CHstatus))
        print('ENERGY EXPENDED PER CHILD NODE: ' + str(erx) + '\n' + 'ENERGY USED FOR TRX: ' + str(etx))
        print('PA: ' + str(node.getPA()) + ', pSize: ' + str(node.pSize) + ', Dist: ' + str(dist) + ', Nr of Children: ' + str(node.conChildren))
        tmp = 'Nrj before: ' + str(eBefore) + '\nNrj after: ' + str(e) + '\nNrj Consumed: ' + str(EC)
        print(tmp)
    
    return e, d, s





for i in range(10):
    #plotEnv(EE)
    #print(f"Round = {EE.rnd}")
    '''
    Loops through the system for ten rounds.   
    It extracts the current state values containing the energy consumed for a 
    node #[nodeNr], data received by a node, and data received by the sink. 
    
    It calculates the predicted values for the coming round. Then it executes
    the node communication, samples the values and compares them to the predictions.
    '''
    EE.updateEnv(1, 1, PRcontrl)
    EE.cluster()
    print('NEW CLUSTERING_____________')
    
    energyBefore = EE.nodes[nodeNr].getEnergy()
    datBefore = EE.nodes[nodeNr].getDataRec()
    sinkDatBefore = EE.sink.getDataRec()
    
    nrjAfter, datAfter, sdatAfter = iterateNodeFunc(EE.nodes[nodeNr], EE)
    diffIt = energyBefore - nrjAfter 
    datDiffIt = datAfter - datBefore
    sdatDiffIt = sdatAfter - sinkDatBefore
    
    EE.communicate()
    

    diffReal = energyBefore - EE.nodes[nodeNr].getEnergy()
    datDiffReal = EE.nodes[nodeNr].getDataRec() - datBefore
    sdatDiffReal= EE.sink.getDataRec() - sinkDatBefore
    print('diff iter: ' + str(diffIt))
    print('Real diff: ' + str(diffReal))
    
    print('DATA diff iter: ' + str(datDiffIt))
    print('DATA Real diff: ' + str(datDiffReal))
    
    print('SINK DATA diff iter: ' + str(sdatDiffIt))
    print('SINK DATA Real diff: ' + str(sdatDiffReal))
    
    
    if(nrjAfter==EE.nodes[nodeNr].getEnergy()):
        print('Energy Prediction for Node nr ' + str(nodeNr) + ' Checks out!')
    if(datAfter==EE.nodes[nodeNr].getDataRec()):
        print('Prediction for Data Received by Node ' + str(nodeNr) + ' Checks Out!')
    if(sdatAfter==EE.sink.getDataRec()):
        print('Prediction for Data Received by the Sink Checks Out!')
    else:
        print('Sink Data Prediction Values Not Equal. Did a node die during transmission just now?')
    EE.iterateRound()
    
    







