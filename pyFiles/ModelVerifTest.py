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