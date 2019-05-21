import sys
sys.path.append("..")  # Adds higher directory to python modules path.

from EnvironmentEngine import *
from plotEnv import *
from setParams import *

EE = EnvironmentEngine()  # Initiate environment

x, y = EE.sink.getPos()  # Get position/coordinates of sink

# Get PR for all nodes (PR should be zero for dead nodes)
#PRcontrl = []
#for i in range(numNodes):
#    PRcontrl.append([i, 10])  # [Node ID, PR of node]


EE.nodes[0].energy = 0.10
print(EE.nodes[0].energy)



while True:  # Run until all node dies
    print(f"Round = {EE.rnd}")

    # print(f"plotRnd Length = {len(EE.plotRnd)}")
    # print(f"meanEClist Length = {len(EE.meanEClist)}")
    # print(f"EClist Length = {len(EE.EClist)}")
    # print(f"PackReclist Length = {len(EE.PackReclist)}")
    # print(f"deadnodes Length = {len(EE.deadNodes)}")

    plotEnv(EE)

    print('ENERGY AT START OF ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
    
    EE.cluster()
    for i in range(time_segments):
        EE.updateEnv(1, 1, PRcontrl)
        EE.communicate()
        print('ENERGY AT TIME SEGMENT {0}: {1}'.format(i, EE.nodes[0].energy))
    
    print('ENERGY AT END OF ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
    
    EE.iterateRound()

    if len(EE.deadNodes) == numNodes:  # Break when all nodes have died
        print('ENERGY AT BREAKPOINT, ROUND {0}: {1}'.format(EE.rnd, EE.nodes[0].energy))
        break

