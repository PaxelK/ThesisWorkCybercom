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
from MPCnodeJH_2 import MPCnode
from MPCsink import MPCsink
from setParamsMPC import *
from MPC2ndLayer_2D import MPC2ndLayer
from plotEnv import *

ctrlHrz = 10
ctrlRes = ctrlHrz + 1
EE = MPC2ndLayer(ctrlHrz, ctrlRes)  # Initiate environment

x, y = EE.sink.getPos()  # Get position/coordinates of sink

# Get PR for all nodes (PR should be zero for dead nodes)
#PRcontrl = []
#for i in range(numNodes):
#    PRcontrl.append([i, 10])  # [Node ID, PR of node]


#EE.nodes[0].energy = 0.10
#print(EE.nodes[0].energy)



while True:  # Run until all node dies
    print(f"Round = {EE.rnd}")

    # print(f"plotRnd Length = {len(EE.plotRnd)}")
    # print(f"meanEClist Length = {len(EE.meanEClist)}")
    # print(f"EClist Length = {len(EE.EClist)}")
    # print(f"PackReclist Length = {len(EE.PackReclist)}")
    # print(f"deadnodes Length = {len(EE.deadNodes)}")

    plotEnv(EE)

    #print('ENERGY AT START OF ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
    
    EE.cluster()
    EE.refreshSolvers()
    optimalP = EE.controlEnv()
    EE.sink.setTarPoint(optimalP[0], optimalP[1])
    for i in range(time_segments):
        print('TIME SEGMENT: {0}'.format(i))
        EE.sink.produce_MoveVector()
        EE.sink.move(EE.sink.xMove.value[1], EE.sink.yMove.value[1])
        EE.communicate()
        #print('ENERGY AT TIME SEGMENT {0}: {1}'.format(i, EE.nodes[0].energy))
    #print('ENERGY AT END OF ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
    
    EE.iterateRound()
    
    
    
    if len(EE.deadNodes) == numNodes:  # Break when all nodes have died
        print('ENERGY AT BREAKPOINT, ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
        break

