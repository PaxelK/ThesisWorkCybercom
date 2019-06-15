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
import csv


ctrlHrz = 10
ctrlRes = ctrlHrz + 1
EE_MPC = MPC2ndLayer(ctrlHrz, ctrlRes)  # Initiate environment
EE_leach = copy.deepcopy(EE_MPC)


x, y = EE_MPC.sink.getPos()  # Get position/coordinates of sink


totRounds_MPC = []
totRounds_leach = []

totPacks_MPC = []
totPacks_leach = []

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
for test in range(1):
    #while True:  # Run until all node dies
    for i in range(2):
        print(f"Round = {EE_MPC.rnd}")
        #plotEnv(EE_MPC)
        #plotEnv(EE_leach)
        
        
        if(len(EE_MPC.deadNodes) != numNodes):
            EE_MPC.cluster()
            optimalP = EE_MPC.controlEnv()
            EE_MPC.sink.setTarPoint(optimalP[0], optimalP[1])
            
            print('Expected lifetime in rounds: {0}'.format(EE_MPC.expLifetime))
            print('Packages received by sink: {0}'.format(EE_MPC.sink.dataRec))
            print('Alive nodes: {0}\nDeadNodes: {1}'.format(len(EE_MPC.nodesAlive), len(EE_MPC.deadNodes)))
            print('Number of nodes alive: {0}'.format(len(EE_MPC.nodesAlive)))
            
            EE_MPC.newCycle = True
            for i in range(time_segments): #time_segments
                print('TIME SEGMENT: {0}'.format(i))
                if i==0:
                    for n in EE_MPC.nonCHds:
                        if n.alive:
                            outcome = n.sendMsg(EE_MPC.sink)
                            if not outcome and EE_MPC.verbose:
                                print(f"Node {n.ID} failed to send to node {n.CHparent.ID}!\n")
                                actionmsg = n.getActionMsg()
                                print(str(actionmsg) + "\n")   
        
        

            
        
                EE_MPC.sink.produce_MoveVector()
                for c in EE_MPC.CHds:
                    if i == 1:
                        c.tempDataRec = 0
                    if c.alive:
                        c.controlPR(EE_MPC.sink)
                        #print(c.data.value)
                        #print('\n')
                        #c.plot()
                        #print(c.data.value)
                        outcome = c.sendMsg(EE_MPC.sink)
                        if not outcome and EE_MPC.verbose:
                            print(f"Node {c.ID} failed to send to node {c.CHparent.ID}!\n")
                            actionmsg = c.getActionMsg()
                            print(str(actionmsg) + "\n")
        
                EE_MPC.sink.move(EE_MPC.sink.xMove.value[1], EE_MPC.sink.yMove.value[1])
            
            
            EE_MPC.iterateRound()
        
        if(len(EE_leach.deadNodes) != numNodes):
            EE_leach.cluster()     
            for c in EE_leach.CHds:
                    c.PA = maxPR

            EE_leach.newCycle = True
            EE_leach.communicate()
            EE_leach.iterateRound()
            print('Finished leach round.')
        
        
        
        """
        If the number of dead nodes reaches the total number of nodes, the network is seen as
        dead and the loop ceases.
        """
        if len(EE_MPC.deadNodes) == numNodes and len(EE_leach.deadNodes) == numNodes:  # Break when all nodes have died
                print('MPC BREAKPOINT AT ROUND {0}'.format(EE_MPC.rnd))
                print('LEACH BREAKPOINT AT ROUND {0}'.format(EE_leach.rnd))
                totRounds_MPC.append(EE_MPC.rnd)
                totRounds_leach.append(EE_leach.rnd)
                
                totPacks_MPC.append(EE_MPC.sink.dataRec/ps)
                totPacks_leach.append(EE_leach.sink.dataRec/ps)
                break
    tempStr = 'Results_MPCVSleachHrz10_reg_' + str(test) + '.txt'
    with open(tempStr, 'w', newline='') as f:
        results = csv.writer(f)
        
        results.writerow(['MPC: ', totRounds_MPC])
        results.writerow(['MPC data Rec [packets]: ', totPacks_MPC])
        results.writerow(['LEACH: ', totRounds_leach])
        results.writerow(['LEACH data Rec [packets]: ', totPacks_leach])
    
    
    
    