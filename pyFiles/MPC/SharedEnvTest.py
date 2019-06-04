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
import copy


ctrlHrz = 10
ctrlRes = ctrlHrz + 1
EE_MPC = MPC2ndLayer(ctrlHrz, ctrlRes)  # Initiate environment
EE_leach = copy.deepcopy(EE_MPC)


x, y = EE_MPC.sink.getPos()  # Get position/coordinates of sink


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
    print(f"Round = {EE_MPC.rnd}")
    plotEnv(EE_MPC)
    plotEnv(EE_leach)
    
    EE_MPC.cluster()
    

    """
    The pseudo-clustering process for the LEACH-environment
    ############################################################
    """
    
    EE_leach.CHds = []       # Reset lists of current CHs and non-CHs
    EE_leach.nonCHds = []
        
        # Check if node is alive, then generate its CHs
    for i in range(len(EE_leach.nodes)):
        EE_leach.nodes[i].resetConChildren()
        EE_leach.nodes[i].clearTempDataRec()
        
        """
        If each CH chosen is alive in both systems, the loop keeps on
        going with the same hierarchy roles.
        """
        EE_leach.nodes[i].CHstatus = EE_MPC.nodes[i].CHstatus          
    """
    Connection phase for the LEACH network's nodes. Pretty much copied from the Cluster() method
    """
    for i in range(len(EE_leach.nodes)):  # Non-CH nodes connect to nearest CH/sink and CHs connect to sink
            if EE_leach.nodes[i].getCHstatus() == 0:  # If node is a simple node (non-CH)
                EE_leach.nonCHds.append(EE_leach.nodes[i]) # Add to list of current non-CHs
                minDistance = EE_leach.nodes[i].getDistance(EE_leach.sink)  # Starts off with the distance to sink
                jshortest = -1  # jshortest starts of as a "non index" number
                for j in range(len(EE_leach.nodes)):
                    if EE_leach.nodes[j].getCHstatus() == 1:  # Checks all cluster head nodes
                        if minDistance > EE_leach.nodes[i].getDistance(EE_leach.nodes[j]):
                            # If distance to cluster head j was shorter than what has been measured before, make
                            # this the new minimum distance
                            minDistance = EE_leach.nodes[i].getDistance(EE_leach.nodes[j])
                            jshortest = j # Store index of this node

                if jshortest >= 0:  # If a CH with in-between distance shorter than that to the sink, connect to this CH
                    EE_leach.nodes[i].connect(EE_leach.nodes[jshortest])
                else:
                    EE_leach.nodes[i].connect(EE_leach.sink)  # Otherwise connect to the sink
            else:  # If node is CH, connect to sink and add to list of current CHs
                EE_leach.nodes[i].connect(EE_leach.sink)
                EE_leach.CHds.append(EE_leach.nodes[i])          
            
    """        
    ##############################################################        
    """              
            
            
    
    EE_MPC.refreshSolvers()
    optimalP = EE_MPC.controlEnv()
    EE_MPC.sink.setTarPoint(optimalP[0], optimalP[1])
    print('Expected lifetime in rounds: {0}'.format(EE_MPC.expLifetime))
    print('Packages received by sink: {0}'.format(EE_MPC.sink.dataRec))
    print('Alive nodes: {0}\nDeadNodes: {1}'.format(len(EE_MPC.nodesAlive), len(EE_MPC.deadNodes)))
    print('Number of nodes alive: {0}'.format(len(EE_MPC.nodesAlive)))
    
    #if(len(EE_MPC.CHds)>0):
    #    print(EE_MPC.CHds[0].desData)
    for i in range(10): #time_segments
        print('TIME SEGMENT: {0}'.format(i))
        EE_MPC.sink.produce_MoveVector()
        for c in EE_MPC.CHds:
            c.controlPR(EE_MPC.sink)
            #print(c.data.value)
            print('\n')
            #c.plot()
            #print(c.data.value)
        EE_MPC.communicate()
        EE_MPC.sink.move(EE_MPC.sink.xMove.value[1], EE_MPC.sink.yMove.value[1])
        
        EE_leach.communicate()
        
    #print('ENERGY AT TIME SEGMENT {0}: {1}'.format(i, EE_MPC.nodes[0].energy))
    #print('ENERGY AT END OF ROUND {0}: {1}'.format(EE_MPC.rnd, EE_MPC.nodes[0].energy))
    
    EE_MPC.iterateRound()
    EE_leach.iterateRound()
    
    """
    If the number of dead nodes reaches the total number of nodes, the network is seen as
    dead and the loop ceases.
    """
    if (len(EE_MPC.deadNodes) > 0 or len(EE_leach.deadNodes >0)):  # Break when one node has died
        print('ENERGY AT BREAKPOINT, ROUND {0}: {1}'.format(EE_MPC.rnd, EE_MPC.nodes[0].energy))
        break