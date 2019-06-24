import csv
import sys

sys.path.append("..")  # Adds higher directory to python modules path.

from random import *
from EnvironmentEngine import *
from setParams import *
from plotEnv import *


def run():
    EE = EnvironmentEngine()  # Initiate environment

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


    # Change default sink position to being in middle of grid
    EE.sink.xPos = xSize / 2
    EE.sink.yPos = ySize / 2

    PRcontrol = []

    while True:  # Run until all node dies

        timeSegTemp = 0

        for i in range(time_segments):

            if i == 0:
                EE.cluster()

            if timeSegTemp == time_segments - 1:  # Send one package at the end of each round
                for i in range(numNodes):
                    PRcontrol = []
                    PRcontrol.append([i, 1])  # [Node ID, PR of node]
            if timeSegTemp == 0:
                for i in range(numNodes):
                    PRcontrol = []
                    PRcontrol.append([i, 0])  # [Node ID, PR of node]

            EE.updateEnv(0, 0, PRcontrol)

            if timeSegTemp == time_segments - 1:  # Non CH sending at end of each round
                for i in range(len(EE.nodes)):
                    if EE.nodes[i].alive:
                        if (EE.nodes[i].CHstatus == 0):
                            outcome = EE.nodes[i].sendMsg(EE.sink)
                            if not outcome:
                                print(f"Node {EE.nodes[i].ID} failed to send to node {EE.nodes[i].CHparent.ID}!\n")
                                actionmsg = EE.nodes[i].getActionMsg()
                                print(str(actionmsg) + "\n")

            for i in range(len( EE.nodes)):  # CH sending
                if EE.nodes[i].alive:
                    if (EE.nodes[i].CHstatus == 1):
                        outcome = EE.nodes[i].sendMsg(EE.sink)
                        if not outcome:
                            print(f"Node {EE.nodes[i].ID} failed to send to node {EE.nodes[i].CHparent.ID}!\n")
                            actionmsg = EE.nodes[i].getActionMsg()
                            print(str(actionmsg) + "\n")

            timeSegTemp += 1

        EE.iterateRound()
        #print(f"rnd: {EE.rnd}")

        if len(EE.deadNodes) == numNodes:  # Break when all nodes have died
            break

    print(f"Rounds survived: {EE.rnd}")
    print(f"Data packets received: {EE.sink.dataRec / 1000}")

    '''             
    # Uncomment if results shall be saved                                                                                                                  
    with open('LEACHresults.txt', 'a', newline='') as f:                                                                              
        f.write(str(EE.rnd) + ",")                                                                                                    
        f.write(str(EE.sink.dataRec/1000) + ",")                                                                                      
    '''

if __name__ == "__main__":
    run()
