import gym
from gym.utils import seeding
import numpy as np
from random import *
from gym.envs.toy_text import discrete

import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *
from EnvironmentEngine import *
from plotEnv import *

EE = EnvironmentEngine()


# Continous WSN class
class WSN(discrete.DiscreteEnv):
    '''
    # Observations:
    Type: Box(4)
    Observation         Min     Max
    X position          0       xSize
    Y position          0       ySize
    (CHstatus           0       1)
    PR                  0       3

    # Actions:
    Type: Discrete(6)
    0 = Move south
    1 = Move north
    2 = Move east
    3 = Move west
    4 = Increase packet rate
    5 = Decrease Packet rate
    '''
    def __init__(self):

        # Maximum size of WSN system
        maxRow = xSize
        maxCol = ySize

        # Define amount of rows and columns that the system consists of
        self.numRows = int(xSize/2)
        self.numCols = int(ySize/2)

        # Check if these members are needed
        self.rnd = 0
        self.numNodes = numNodes

        self.PRamount = 4  # Amount of values PR can be

        numActions = 6
        numStates = int(self.numRows * self.numCols * (numNodes * self.PRamount) * (numNodes * 2))


        P = {state: {action: []
                     for action in range(numActions)} for state in range(numStates)}

        for row in range(self.numRows):
            for col in range(self.numCols):
                for node in range(len(EE.nodes)):
                    for action in range(numActions):
                        PR = EE.nodes[node].PA
                        state = self.encode(row, col, PR)
                        newRow, newCol, newPacketRates = row, col, PR
                        reward = -1  # Default reward for moving sink
                        done = False  # Boolean for if episode is complete
                        sinkLoc = (row, col)  # Position of sink

                        # Actions: 0 = Move south, 1 = Move north, 2 = Move east, 3 = Move west,
                        # 4 = Increase packet rate, 5 Decrease Packet rate
                        if action == 0:  # Move sink south
                            newRow = min(row + 1, maxRow)
                        elif action == 1:  # Move sink north
                            newRow = max(row - 1, 0)
                        if action == 2:  # Move sink east
                            newCol = min(col + 1, maxCol)
                        elif action == 3:  # Move sink west
                            newCol = max(col - 1, 0)
                        if action == 4:  # Increase PR of specific node
                            EE.nodes[node].PA = min(self.PRamount - 1, EE.nodes[node].PA + 1)  # PR can be zero
                            newPacketRates = EE.nodes[node].PA
                            reward = 10
                        elif action == 5:  # Decrease PR of specific node
                            EE.nodes[node].PA = max(0, EE.nodes[node].PA - 1)
                            newPacketRates = EE.nodes[node].PA
                            reward = -10

                        newState = self.encode(newRow, newCol, newPacketRates)
                        P[state][action].append((1.0, newState, reward, done))


        initialStateDistrib = np.zeros(numStates)
        #initialStateDistrib /= initialStateDistrib.sum()
        discrete.DiscreteEnv.__init__(self, numStates, numActions, P, initialStateDistrib)

        self.seed()
        self.done = False
        self.state = EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        for i in range(numNodes):
            self.state.append(EE.nodes[i].PA)

    def encode(self, row, col, PR):
        # (5) 5, 5, 4
        i = row
        i *= self.numCols
        i += col
        i *= self.PRamount
        i += PR
        return i

    def decode(self, i):
        out = []
        out.append(i % self.PRamount)
        i = i // self.PRamount
        out.append(i % self.numCols)
        i = i // self.numCols
        out.append(i)
        assert 0 <= i < self.numRows
        return reversed(out)  # [row, col, PR]

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        self.rnd += 1

        self.state = EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        for i in range(numNodes):
            self.state.append([EE.nodes[i].ID, EE.nodes[i].PA])

        xPos, yPos, PR = self.state
        PR = [PR]  # Convert to list

        # Default values
        reward = 0
        done = False

        if len(EE.deadNodes) == numNodes:
            done = True

        if action == 0:
            self.state[1] -= 1  # yPos -
            EE.updateEnv(0, -1, PR)


        elif action == 1:
            self.state[1] += 1  # yPos +
            EE.updateEnv(0, 1, PR)

        elif action == 2:
            self.state[0] += 1  # xPos +
            EE.updateEnv(1, 0, PR)

        elif action == 3:
            self.state[0] -= 1  # xPos -
            EE.updateEnv(-1, 0, PR)

        # PR is hard coded for one node
        elif action == 4:
            reward = 10
            EE.nodes[0].PA = min(self.PRamount - 1, EE.nodes[0].PA + 1)
            self.state[2][1] = EE.nodes[0].PA  # PR +
            EE.updateEnv(0, 0, PR)

        elif action == 5:
            reward = -10
            EE.nodes[0].PA = max(0, EE.nodes[0].PA - 1)
            self.state[2][1] = EE.nodes[0].PA  # PR -
            EE.updateEnv(0, 0, PR)

        EE.cluster()
        EE.communicate()
        EE.iterateRound()

        row, col, PR = self.state[0], self.state[1], self.state[2][1]
        #print(self.state)
        #print("---------------------")
        return np.array(self.encode(row, col, PR)), reward, done, {}

    def reset(self):
        '''
        Resets the entire WSN by placing the sink in a random position and all nodes have a random PR
        '''
        self.rnd = 0
        EE.rnd = 0
        self.state = [random.randint(0, xSize), random.randint(0, ySize)]
        for i in range(numNodes):
            self.state.append([i, random.randint(0, self.PRamount - 1)])

            # Resets the nodes. Needs to be fixed for random energy
            EE.nodes[i].energy = EE.nodes[i].maxEnergy
            EE.nodes[i].SoC = EE.nodes[i].energy / EE.nodes[i].maxEnergy
            EE.nodes[i].PS = 0
            EE.nodes[i].CHstatus = 0  # Cluster head status: 1 if CH, 0 if not CH
            EE.nodes[i].CHparent = None  # Reference to the nodes current cluster head
            EE.nodes[i].dataRec = 0  # Data received = amount of data the node has received
            EE.nodes[i].PS = 0  # Packages sent = amount of packages the node has sent
            EE.nodes[i].nrjCons = 0  # Energy consumed [J] = Amount of energy the node has consumed
            EE.nodes[i].actionMsg = ''  # String containing message about connection and sending status
            EE.nodes[i].CHflag = 0  # Determines if node has been CH during a LEACH episode
            EE.nodes[i].conChildren = 0  # Number of connected children.

            if EE.nodes[i].energy > 0:
                EE.nodes[i].alive = True  # Boolean for if node is alive
            else:
                EE.nodes[i].alive = False

        return np.array(self.state)

    def render(self, mode='human'):
        plotEnv(EE)
