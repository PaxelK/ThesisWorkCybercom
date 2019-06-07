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
from MPCnode_v3 import MPCnode
from MPCsink import MPCsink
from MPC2ndLayer_2D_v2 import MPC2ndLayer
from plotEnv import *
from setParamsMPC import *

ctrlHrz = 10
ctrlRes = ctrlHrz + 1
EE = MPC2ndLayer(ctrlHrz, ctrlRes)  # Initiate environment

x, y = EE.sink.getPos()  # Get position/coordinates of sink


"""
The greater loop. One loop represents a round. During this loop the following steps occur:
    1. The environment is plotted, shows change in network energy and packages aggrevated
    2. The network is clustered, e.g. cluster head and non-CH roles are assigned
    3. The solvers for the 2nd layer and the sink are refreshed for the new round
    4. The 2nd layer decides on an optimal sink point-to-be, which gets relayed to the sink control,
        and an optimal amount of data to be desired from each cluster head
    5. The minor loop begins:
            The loop represents each time segment of a round. 
            During this loop the following steps occur:
                a) The sink produces an array containing its planned destination
                    for each time segment. This is for the node later accessing it
                    to be able to plan for optimal transmission timings.
                b) A for-loop is run to execute control on each CHs packet rate
                c) Transmission occurs when all is set; communicate() is called
                d) The sink moves another step on its planned route.
    6. iterateRound() is called to record network stats and prepare the network for the next round.            
"""

#while True:  # Run until all node dies
for i in range(3):
    print(f"Round = {EE.rnd}")
    plotEnv(EE)

    #print('ENERGY AT START OF ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
    
    EE.cluster()
    optimalP = EE.controlEnv()
    EE.sink.setTarPoint(optimalP[0], optimalP[1])
    print('Expected lifetime in rounds: {0}'.format(EE.expLifetime))
    print('Packages received by sink: {0}'.format((EE.sink.dataRec/ps)))
    print('Alive nodes: {0}\nDeadNodes: {1}'.format(len(EE.nodesAlive), len(EE.deadNodes)))
    print('Number of nodes alive: {0}'.format(len(EE.nodesAlive)))
    
    #if(len(EE.CHds)>0):
    #    print(EE.CHds[0].desData)
    for i in range(10): #time_segments
        print('TIME SEGMENT: {0}'.format(i))
        EE.sink.produce_MoveVector()
        for c in EE.CHds:
            c.controlPR(EE.sink)
            #print(c.data.value)
            print('\n')
            #c.plot()
            #print(c.data.value)
        EE.communicate()
        EE.sink.move(EE.sink.xMove.value[1], EE.sink.yMove.value[1])
        
        
    #print('ENERGY AT TIME SEGMENT {0}: {1}'.format(i, EE.nodes[0].energy))
    #print('ENERGY AT END OF ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
    
    EE.iterateRound()
    
    """
    If the number of dead nodes reaches the total number of nodes, the network is seen as
    dead and the loop ceases.
    """
    if len(EE.deadNodes) == numNodes:  # Break when all nodes have died
        print('ENERGY AT BREAKPOINT, ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
        break
