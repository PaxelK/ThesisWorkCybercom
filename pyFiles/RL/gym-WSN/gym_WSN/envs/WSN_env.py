import gym
from gym.utils import seeding
import numpy as np
from gym.envs.toy_text import discrete
from random import *
from gym import spaces

import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *
from EnvironmentEngine import *
from plotEnv import *




# Continous WSN class
class WSN(gym.Env):
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

        self.EE = EnvironmentEngine()


        self.xSize = xSize
        self.ySize = ySize

        self.rnd = 0
        self.numNodes = numNodes
        self.PRamount = 4  # Amount of values PR can be

        # By using a system grid size of 100x100 we get a step size of 2 m
        high = np.array([
            int(self.xSize),
            int(self.ySize),
            self.PRamount])
        #high = np.array([
              #int(self.xSize / 50),
              #int(self.ySize / 50),
              #6])

        low = np.array([
            0,
            0,
            0])

        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.seed()
        self.done = False
        self.viewer = None
        self.state = self.EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        for i in range(numNodes):
            self.state.append(self.EE.nodes[i].PA)


    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        self.rnd += 1

        self.state = self.EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        for i in range(numNodes):
            self.state.append([self.EE.nodes[i].ID, self.EE.nodes[i].PA])

        xPos, yPos, PR = self.state
        PR = [PR]  # Convert to list

        # Default values, Change if there are more than one node
        reward = self.EE.nodes[0].getEnergy() * 0.1
        done = False

        if len(self.EE.deadNodes) == numNodes:
            done = True

        if action == 0:
            self.state[1] = max(0, self.state[1]-2)  # yPos -
            self.EE.updateEnv(0, -2, PR)

        elif action == 1:
            self.state[1] = min(ySize, self.state[1] + 2)  # yPos +
            self.EE.updateEnv(0, 2, PR)

        elif action == 2:
            self.state[0] = min(xSize, self.state[0] + 2)  # xPos +
            self.EE.updateEnv(2, 0, PR)

        elif action == 3:
            self.state[0] = max(0, self.state[0] - 2)  # xPos -
            self.EE.updateEnv(-2, 0, PR)

        # PR is hard coded for one node
        elif action == 4:
            if self.EE.nodes[0].PA < self.PRamount:
                reward += 10
                PR = [[PR[0][0], PR[0][1]+1]]
                self.state[2][1] = self.EE.nodes[0].PA  # PR +
                self.EE.updateEnv(0, 0, PR)
            else:
                reward = -10

        elif action == 5:
            if self.EE.nodes[0].PA > 1:
                reward += -10
                PR = [[PR[0][0], PR[0][1]-1]]
                self.state[2][1] = self.EE.nodes[0].PA  # PR -
                self.EE.updateEnv(0, 0, PR)
            else:
                reward = - 10


        self.EE.cluster()
        self.EE.nodes[0].CHstatus = 1
        self.EE.communicate()
        self.EE.iterateRound()

        '''
        print(f"self.state: {self.state}")
        print(f"self.EE.sink.getPos(): {self.EE.sink.getPos(), self.EE.nodes[0].PA}")
        print("---------------------")
        '''

        return np.array(self.state), reward, done, {}

    def reset(self):
        '''
        Resets the entire WSN by placing the sink in a random position and all nodes have a random PR

        TODO: Reset the environment parameters as well, eg. packets sent, energy consumed etc.
        '''
        '''
        self.EE = EnvironmentEngine()  # Reinitiate environment engine

        self.rnd = 0
        self.done = False
        self.state = self.EE.getStates()[0:2]  # Gets the x and y position of sink
        for i in range(numNodes):
            self.state.append(self.EE.nodes[i].PA)
        '''

        # Currently designed for one node, needs to be changed later
        self.state = [random.randint(0, self.xSize), random.randint(0, self.ySize)]
        for i in range(numNodes):
            self.state.append([i, random.randint(0, self.PRamount)])
            self.EE.nodes[i].energy = maxNrj  #random.random() * maxNrj
            self.EE.nodes[i].SoC = self.EE.nodes[i].energy / self.EE.nodes[i].maxEnergy
            self.EE.PS = 0  # Packages sent = amount of packages the node has sent
            self.EE.nrjCons = 0  # Energy consumed [J] = Amount of energy the node has consumed
            self.EE.CHflag = 0  # Determines if node has been CH during a LEACH episode
            self.EE.conChildren = 0  # Number of connected children.
            self.EE.tempDataRec = 0  # Temporary held data that are then going to the sink.

            if self.EE.nodes[i].energy > 0:
                self.EE.nodes[i].alive = True  # Boolean for if node is alive
            else:
                self.EE.nodes[i].alive = False


        self.EE.rnd = 1  # Round number
        self.EE.nodesAlive = []  # Contains the amount of nodes that are alive after each round
        self.EE.EClist = []  # List that  contains the energy consumed after each round
        self.EE.PackReclist = []  # List that contains the data packets received for the sink after each round
        self.EE.meanEClist = []  # List that contains the mean energy consumed after each round
        self.EE.deadNodes = []  # Contains the amount of dead nodes after each round
        self.EE.posNodes = []  # The position of the nodes


        self.EE.sink.dataRec = 0
        self.EE.sink.nrjCons = 0
        self.EE.sink.xPos = int(xSize * random.random())
        self.EE.sink.yPos = int(ySize * random.random())
        self.EE.sink.SoC = self.EE.sink.energy / self.EE.sink.maxEnergy

        self.EE.plotDeadNodes = []  # Used for plotting amount of dead nodes

        tempNRJ = 0

        for node in self.EE.nodes:  # Iterate over all nodes
            tempNRJ += node.nrjCons
            if node.alive:  # If node is still alive
                self.EE.nodesAlive.append(node)
            else:  # Else node is dead
                self.EE.deadNodes.append(node)

        self.EE.plotDeadNodes = [len(self.EE.deadNodes)]

        nrjMean = 0
        if self.EE.nodesAlive:  # If there are nodes alive
            nrjMean = tempNRJ / len(self.EE.nodesAlive)  # Mean energy consumed by all nodes

        # For plotting purpose
        self.EE.EClist.append(tempNRJ)
        self.EE.PackReclist.append(self.EE.sink.dataRec)
        self.EE.meanEClist.append(nrjMean)

        for node in self.EE.nodesAlive:  # Saves the position of all the nodes in a list
            xnd, ynd = node.getPos()
            self.EE.posNodes.append([xnd, ynd])
        self.EE.posNodes = np.array(self.EE.posNodes)

        # For plotting a fixed time length
        self.EE.plotRnd = [1]

        if (len(self.EE.EClist) or len(self.EE.PackReclist) or len(self.EE.plotDeadNodes) or len(self.EE.meanEClist) or
            len(self.EE.plotRnd)) > plotlen:
            del self.EE.EClist[0]
            del self.EE.PackReclist[0]
            del self.EE.plotDeadNodes[0]
            del self.EE.meanEClist[0]
            del self.EE.plotRnd[0]


        return np.array(self.state)


    def render(self, mode='human'):
        plotEnv(self.EE)










    '''
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
    '''

