import sys
sys.path.append("..")  # Adds higher directory to python modules path.
import gym
import gym_WSN

from EnvironmentEngine import *
from plotEnv import *

ctrl = gym.make('WSN-v0') # Initiate RL environment
ctrl.step(1)



'''
EE = EnvironmentEngine()  # Initiate WSN environment

# Get PR for all nodes (PR should be zero for dead nodes)
PRcontrl = [(1,100)]



states = EE.getStates()

while True:  # Run until all node dies
    print(f"Round = {EE.rnd}")

    #states = EE.getStates()
    #ctrl.step(1)

    EE.updateEnv(1, 1, PRcontrl)
    EE.cluster()
    EE.communicate()
    EE.iterateRound()

    plotEnv(EE)

    if (len(EE.EClist) or len(EE.PackReclist) or len(EE.plotDeadNodes) or len(EE.meanEClist) or len(EE.plotRnd)) > plotlen:
        del EE.EClist[0]
        del EE.PackReclist[0]
        del EE.plotDeadNodes[0]
        del EE.meanEClist[0]
        del EE.plotRnd[0]


    if len(EE.deadNodes) == numNodes: # Break when all nodes have died
        break

'''
