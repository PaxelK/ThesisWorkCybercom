import csv
import sys

sys.path.append("../MPC")  # Adds higher directory to python modules path.
sys.path.append("..")  # Adds higher directory to python modules path.

from random import *
from EnvironmentEngineMPC import *
from setParams import *
from plotEnv import *
import time


def run():
    EE = EnvironmentEngineMPC(10,11)  # Initiate environment

    '''
    with open('../RL/nodePlacement.csv') as nodePlacement_file:
        csv_reader = csv.reader(nodePlacement_file, delimiter=',')
        row_count = 0


        for row in csv_reader:
            i = 0
            rowVec = []

            for element in row:
                rowVec.append(float(element))

            if row_count == 0:
                for valueX in rowVec:
                    EE.nodes[i].xPos = valueX
                    i += 1
            if row_count == 1:
                for valueY in rowVec:
                    EE.nodes[i].yPos = valueY
                    i += 1
            row_count += 1

    '''

    '''
    EE.nodes[0].xPos = 130
    EE.nodes[0].yPos = 130

    EE.nodes[1].xPos = 170
    EE.nodes[1].yPos = 130

    EE.nodes[2].xPos = 130
    EE.nodes[2].yPos = 170

    EE.nodes[3].xPos = 170
    EE.nodes[3].yPos = 170
    '''

    # Change default sink position to being in middle of grid
    EE.sink.xPos = xSize / 2
    EE.sink.yPos = ySize / 2

    PRcontrol = []
    for i in range(numNodes):
        PRcontrol.append([i, 1])  # [Node ID, PR of node]

    while True:  # Run until all node dies

        EE.cluster()



        EE.updateEnv(0, 0, PRcontrol)
        '''
        for i in range(len(EE.nodes)): # Non-CH sending
            if EE.nodes[i].alive:
                if (EE.nodes[i].CHstatus == 0):
                    outcome = EE.nodes[i].sendMsg(EE.sink)
                    if not outcome:
                        print(f"Node {EE.nodes[i].ID} failed to send to node {EE.nodes[i].CHparent.ID}!\n")
                        actionmsg = EE.nodes[i].getActionMsg()
                        print(str(actionmsg) + "\n")

        for i in range(len(EE.nodes)):  # CH sending
            if EE.nodes[i].alive:
                if (EE.nodes[i].CHstatus == 1):
                    outcome = EE.nodes[i].sendMsg(EE.sink)
                    if not outcome:
                        print(f"Node {EE.nodes[i].ID} failed to send to node {EE.nodes[i].CHparent.ID}!\n")
                        actionmsg = EE.nodes[i].getActionMsg()
                        print(str(actionmsg) + "\n")

        '''

        EE.communicate()
        plotEnv(EE, 1)
        time.sleep(3)

        EE.iterateRound()

        print(f"rnd: {EE.rnd}")

        if len(EE.deadNodes) == numNodes:  # Break when all nodes have died
            break

    print(f"Rounds survived: {EE.rnd}")
    print(f"Data packets received: {EE.sink.dataRec / 1000}")



run()
