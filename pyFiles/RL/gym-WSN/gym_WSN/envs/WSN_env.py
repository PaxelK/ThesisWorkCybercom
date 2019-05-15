# Import the WSN RL env
import gym
from gym.utils import seeding
# Import needed libraries
import numpy as np
from gym.envs.toy_text import discrete
from random import *
from gym import spaces
# Import needed files
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *
from EnvironmentEngine import *
from plotEnv import *

# Continous WSN class
class WSN(gym.Env):
    '''
    # Observations:
    Type: Box
    Observation         Min     Max         Notes
    X position          0       xSize
    Y position          0       ySize
    CHstatus            0       1           The same amount as amount of nodes
    PR                  0       3           Amount is amount of nodes multiplied with self.PRamount

    # Actions:
    Type: Discrete(6)
    0 = Move south
    1 = Move north
    2 = Move east
    3 = Move west
    4 = Increase packet rate  (One for each node)
    5 = Decrease Packet rate  (One for each node)
    '''
    def __init__(self):
        # Init the WSN env
        self.EE = EnvironmentEngine()

        # Define size of WSN grid in meters
        self.xSize = xSize
        self.ySize = ySize

        self.numNodes = numNodes  # Number of nodes
        self.PRamount = 4  # Amount of values PR can be

        # Define the high values of each state
        high = [int(self.xSize), int(self.ySize)]
        for i in range(numNodes):
            high.append(self.PRamount)
        for ii in range(numNodes):
            high.append(1)  # CH status
        high = np.array(high)

        # Define the low values of each state
        low = []
        for i in range(2+(2*numNodes)):
            low.append(0)
        low = np.array(low)

        # Create action space (discrete) and observation space (Box/continuos)
        self.action_space = spaces.Discrete(4+(2*numNodes))
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        # Set default values
        self.seed()
        self.done = False
        self.viewer = None
        self.state = self.EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        for i in range(numNodes):  # Appends PA of all nodes into list
            self.state.append(self.EE.nodes[i].PA)
        for ii in range(numNodes):
            self.state.append(self.EE.nodes[ii].getCHstatus())


    def seed(self, seed=None):  # Returns initial state of env
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        '''
        This method steps through the entire WSN environment when a specific action is taken. This includes the reward,
        clustering, communication etc.
        :param action: The action that is performed at the specific step
        :return:  Numpy array containing the current state, reward, bool for if episode is done and development info
        '''
        # Assert that chosen action is within action space
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        # Get state of current time step
        self.state = self.EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        # Get PR of every node
        PRtemp  = []
        CHtemp = []
        for i in range(numNodes):
                PRtemp.append([self.EE.nodes[i].ID, self.EE.nodes[i].PA])
                CHtemp.append(self.EE.nodes[i].getCHstatus())
        self.state.append(PRtemp)
        self.state.append(CHtemp)
        _, _, PR, _ = self.state

        # Cluster nodes in WSN env
        self.EE.cluster()
        #self.EE.nodes[0].CHstatus = 1
        #self.EE.nodes[1].CHstatus = 1

        # Default values
        reward = -2
        for i in range(numNodes):
            if self.EE.nodes[i].CHstatus == 1:
                reward -= (self.EE.nodes[i].getDistance(self.EE.sink))# * 0.05)  # Distance to each CH
        #reward += (self.EE.nodes[0].getEnergy() * 0.0001)
        done = False

        if len(self.EE.deadNodes) == numNodes:  # Episode is done if all nodes have died
            done = True

        if action == 0:  # This action is yPos -= 1
            if self.state[1] > 0:
                self.state[1] -= 1
                self.EE.updateEnv(0, -1, PR)
            else:
                reward = -20

        elif action == 1: # This action is yPos += 1
            if self.state[1] < ySize:
                self.state[1] += 1
                self.EE.updateEnv(0, 1, PR)
            else:
                reward = -20

        elif action == 2:  # This action is xPos += 1
            if self.state[0] < xSize:
                self.state[0] += 1
                self.EE.updateEnv(1, 0, PR)
            else:
                reward = -20

        elif action == 3:  # This action is xPos -= 1
            if self.state[0] > 0:
                self.state[0] -= 1
                self.EE.updateEnv(-1, 0, PR)
            else:
                reward = -20

        if not (action == 0 or action == 1 or action == 2 or action == 3):
            act_temp = 0
            for i in range(numNodes):
                if action == i + act_temp + 4:  # This action is PR += 1
                    if self.EE.nodes[i].PA < self.PRamount:
                        reward += 5
                        PR[i][1] += 1
                        self.state[2][i][1] = self.EE.nodes[i].PA + 1
                        self.EE.updateEnv(0, 0, PR)
                    else:
                        reward = -50
                    break

                elif action == i + act_temp + 5:  # This action is PR -= 1
                    if self.EE.nodes[i].PA > 1:
                        reward -= 5
                        PR[i][1] -= 1
                        self.state[2][i][1] = self.EE.nodes[i].PA - 1
                        self.EE.updateEnv(0, 0, PR)
                    else:
                        reward = -50
                    break
                act_temp += 1


        # Increment WSN env
        self.EE.communicate()
        self.EE.iterateRound()

        return np.array(self.state), reward, done, {}

    def reset(self):
        '''
        Resets the entire WSN by placing the sink in a random position and all nodes have a random PR
        '''

        self.state = [random.randint(0, self.xSize), random.randint(0, self.ySize)]
        for i in range(numNodes):
            self.state.append([i, random.randint(0, self.PRamount)])
            self.EE.nodes[i].energy = maxNrj  #random.random() * maxNrj
            self.EE.nodes[i].SoC = self.EE.nodes[i].energy / self.EE.nodes[i].maxEnergy
            self.EE.nodes[i].PS = 0  # Packages sent = amount of packages the node has sent
            self.EE.nodes[i].nrjCons = 0  # Energy consumed [J] = Amount of energy the node has consumed
            self.EE.nodes[i].CHflag = 0  # Determines if node has been CH during a LEACH episode
            self.EE.nodes[i].conChildren = 0  # Number of connected children.
            self.EE.nodes[i].tempDataRec = 0  # Temporary held data that are then going to the sink.

            if self.EE.nodes[i].energy > 0:
                self.EE.nodes[i].alive = True  # Boolean for if node is alive
            else:
                self.EE.nodes[i].alive = False
        for ii in range(numNodes):
            self.state.append(self.EE.nodes[ii].getCHstatus())


        self.EE.rnd = 1  # Round number
        self.EE.nodesAlive = []  # Contains the amount of nodes that are alive after each round
        self.EE.EClist = []  # List that  contains the energy consumed after each round
        self.EE.PackReclist = []  # List that contains the data packets received for the sink after each round
        self.EE.meanEClist = []  # List that contains the mean energy consumed after each round
        self.EE.deadNodes = []  # Contains the amount of dead nodes after each round
        self.EE.posNodes = []  # The position of the nodes
        self.EE.plotDeadNodes = []  # Used for plotting amount of dead nodes


        self.EE.sink.dataRec = 0
        self.EE.sink.nrjCons = 0
        self.EE.sink.xPos = int(xSize * random.random())
        self.EE.sink.yPos = int(ySize * random.random())
        self.EE.sink.SoC = self.EE.sink.energy / self.EE.sink.maxEnergy


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
        '''
        This method plots the WSN env
        :return: None
        '''
        plotEnv(self.EE)


