import csv
import sys

sys.path.append("..")  # Adds higher directory to python modules path.
sys.path.append("../MPC")  # Adds higher directory to python modules path.

from random import *
from EnvironmentEngineMPC import *
from setParams import *
from plotEnv import *

class LEACHtest():
    def __init__(self):
        self.timeSegTemp = 0
        self.EE = EnvironmentEngineMPC(10, 11)  # Initiate environment
        self.PPJ = []
        self.nrjList =[]
        self.dataList = []

    def placeNodes(self):
        with open('../RL/fixNodePlacement.csv') as nodePlacement_file:
            csv_reader = csv.reader(nodePlacement_file, delimiter=',')
            row_count = 0

            for row in csv_reader:
                i = 0
                rowVec = []

                for element in row:
                    rowVec.append(float(element))

                if row_count == 0:
                    for valueX in rowVec:
                        self.EE.nodes[i].xPos = valueX
                        i += 1
                if row_count == 1:
                    for valueY in rowVec:
                        self.EE.nodes[i].yPos = valueY
                        i += 1
                row_count += 1

        # Change default sink position to being in middle of grid
        self.EE.sink.xPos = xSize / 2
        self.EE.sink.yPos = ySize / 2



    def step(self, CHlist):
        PRcontrol = []

        if self.timeSegTemp == 0: # Cluster at each round (not time segment)
            energy = []

            if self.EE.rnd == 1:
                self.nrjList.append(0)
                self.dataList.append(0)
                self.PPJ.append(0)
            else:
                for i in range(numNodes):
                    energy.append(self.EE.nodes[i].nrjCons)
                self.nrjList.append(sum(energy))
                self.dataList.append(self.EE.sink.dataRec)

                self.PPJ.append((self.dataList[-1]-self.dataList[-2])/(self.nrjList[-1]-self.nrjList[-2]))

            # Change CH status of nodes (Uncomment if until all node dies)
            self.EE.cluster()
            '''
            for i in range(len(self.EE.nodes)):
                self.EE.nodes[i].resetConChildren()
                self.EE.nodes[i].clearTempDataRec()
                if self.EE.nodes[i].alive and CHlist[i] == 1:  # Generate CH status if node is alive and CH in DQN
                    self.EE.nodes[i].CHstatus = 1
                else:  # If node is not alive or not CH in DQN, node cannot be CH
                    self.EE.nodes[i].CHstatus = 0


            for i in range(len(self.EE.nodes)):  # Non-CH nodes connect to nearest CH/sink and CHs connect to sink
                if self.EE.nodes[i].getCHstatus() == 0:  # If node is a simple node (non-CH)
                    minDistance = self.EE.nodes[i].getDistance(self.EE.sink)  # Starts off with the distance to sink
                    jshortest = -1  # jshortest starts of as a "non index" number
                    for j in range(len(self.EE.nodes)):
                        if self.EE.nodes[j].getCHstatus() == 1:  # Checks all cluster head nodes
                            if minDistance > self.EE.nodes[i].getDistance(self.EE.nodes[j]):
                                # If distance to cluster head j was shorter than what has been measured before, make
                                # this the new minimum distance
                                minDistance = self.EE.nodes[i].getDistance(self.EE.nodes[j])
                                jshortest = j  # Store index of this node

                    if jshortest > 0:  # If a CH with in -between distance shorter than that to the sink, connect to this CH
                        self.EE.nodes[i].connect(self.EE.nodes[jshortest])
                    else:
                        self.EE.nodes[i].connect(self.EE.sink)  # Otherwise connect to the sink
                else:  # If node is CH, connect to sink
                    self.EE.nodes[i].connect(self.EE.sink)
            '''

        # -------------------------------Identical CH status generation ends here--------------------------------

        if self.timeSegTemp == time_segments - 1:  # All ndoes send one package at the end of each round
            for i in range(numNodes):
                PRcontrol.append([i, 1])  # [Node ID, PR of node]
        if self.timeSegTemp == 0:
            for i in range(numNodes):
                PRcontrol.append([i, 0])

        self.EE.updateEnv(0, 0, PRcontrol)  # Update environment based without moving sink

        if self.timeSegTemp == time_segments - 1:  # Non CH sending at end of each round
            for i in range(len(self.EE.nodes)):
                if self.EE.nodes[i].alive:
                    if (self.EE.nodes[i].CHstatus == 0):
                        outcome = self.EE.nodes[i].sendMsg(self.EE.sink)
                        if not outcome:
                            print(f"Node {self.EE.nodes[i].ID} failed to send to node {self.EE.nodes[i].CHparent.ID}!\n")
                            actionmsg = self.EE.nodes[i].getActionMsg()
                            print(str(actionmsg) + "\n")

        for i in range(len(self.EE.nodes)):  # CH can send during any time segment
            if self.EE.nodes[i].alive:
                if (self.EE.nodes[i].CHstatus == 1):
                    outcome = self.EE.nodes[i].sendMsg(self.EE.sink)
                    if not outcome:
                        print(f"Node {self.EE.nodes[i].ID} failed to send to node {self.EE.nodes[i].CHparent.ID}!\n")
                        actionmsg = self.EE.nodes[i].getActionMsg()
                        print(str(actionmsg) + "\n")

        self.timeSegTemp += 1

        if self.timeSegTemp == time_segments:
            self.timeSegTemp = 0
            self.EE.iterateRound()


        # When one node have died the episode has finished (can be changed to all nodes died)
        if len(self.EE.deadNodes) == numNodes: #>= 1:
            '''
            with open('PPJresultsLEACH.txt', 'a', newline='') as f:
                f.write(str(self.PPJ) + ",")
                f.write(str(self.nrjList) + ",")
                f.write(str(self.dataList) + ",")
            '''

            return True  # Return True if LEACH is finished
        else:
            return False  # Otherwise return False



def create():
    return LEACHtest()

if __name__ == "__main__":
    LEACHtest()
