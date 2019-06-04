# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:25:41 2019

@author: axkar1
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from Node import Node
from Sink import Sink
from EnvironmentEngine import EnvironmentEngine
from plotEnv import *
from setParams import *

EE = EnvironmentEngine()
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

while True:  # Run until all node dies
#for i in range(3):
    print(f"Round = {EE.rnd}")
    #plotEnv(EE)

    #print('ENERGY AT START OF ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
    
    EE.cluster()
    
    for i in range(10): #time_segments
        print('TIME SEGMENT: {0}'.format(i))
        EE.communicate()
    
    EE.iterateRound()
    
    """
    If the number of dead nodes reaches the total number of nodes, the network is seen as
    dead and the loop ceases.
    """
    if len(EE.deadNodes) == numNodes:  # Break when all nodes have died
        print('ENERGY AT BREAKPOINT AT ROUND {0}'.format(EE.rnd))
        break
