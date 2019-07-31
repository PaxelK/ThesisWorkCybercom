# Import the WSN RL env
import gym
from gym.utils import seeding
# Import needed libraries
import numpy as np
from gym.envs.toy_text import discrete
from random import *
from gym import spaces
import math
# Import needed files
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
sys.path.append("../MPC")  # Adds higher directory to python modules path.
from setParams import *
from EnvironmentEngineMPC import *
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
    PR                  0       3           Amount is amount of nodes multiplied with maxPR
    Sink speed          1       5

    # Actions:
    Type: Discrete(6)
    0 = Move south
    1 = Move north
    2 = Move east
    3 = Move west
        Move diagonally
    4 = Increase packet rate  (One for each node)
    5 = Decrease Packet rate  (One for each node)
    n = Move sink with different speeds in all directions
    '''
    def __init__(self):
        # Init the WSN env
        self.EE = EnvironmentEngineMPC(10, 11)

        # Used when time segments are implemented
        self.timeSegTemp = 0 # Current time segment
        self.sendStatus = [False] * numNodes # List containing status if node has sent a packet during current round
        self.CHtemp = []
        self.PPJ = []
        self.nrjList = []
        self.dataList = []

        # Define size of WSN grid in meters
        self.xSize = xSize
        self.ySize = ySize

        self.numNodes = numNodes  # Number of nodes
        self.rndCounter = 0
        self.sinkSpeed = 1

        # Define the high values of each state
        high = [int(self.xSize), int(self.ySize)]
        for i in range(numNodes):
            high.append(maxPR)
        for ii in range(numNodes):
            high.append(1)  # CH status
        high.append(5) # Sink Speed
        high = np.array(high)

        # Define the low values of each state
        low = []
        for i in range(2+(2*numNodes)):
            low.append(0)
        low.append(1)
        low = np.array(low)

        # Create action space (discrete) and observation space (Box/continuos)
        self.action_space = spaces.Discrete(40+(2*numNodes)) # 40 (sink speed) 2*numNodes(INcrease and decrease PR)
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
        self.state.append(self.sinkSpeed) # Sink speed is 1 per default

        self.tempActList = [] #[0, 1, 2, 3]
        for i in range(8):
            self.tempActList.append(i)


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

        if self.timeSegTemp == time_segments: # New round starts if currentTimeSegment = timeSegment
            self.EE.iterateRound()
            self.rndCounter += 1  # Rnd counter for RL env (In this class)
            self.timeSegTemp = 0

        if self.timeSegTemp == 0:
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

            # Cluster nodes in WSN env after every round is finished
            self.EE.cluster()
            self.sendStatus = [False] * numNodes # Reset transmission status after each round


        # Get state of current time step (for action)
        self.state = self.EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        # Get PR of every node
        PRtemp  = []
        self.CHtemp = []
        for i in range(numNodes):
                PRtemp.append([self.EE.nodes[i].ID, self.EE.nodes[i].PA])
                self.CHtemp.append(self.EE.nodes[i].getCHstatus())
        self.state.append(PRtemp)
        self.state.append(self.CHtemp)
        self.state.append(self.sinkSpeed)
        _, _, PR, _, _ = self.state

        # Default values
        reward = -20
        done = False


        if len(self.EE.deadNodes) == numNodes: #>= 1:   # Episode is done if all nodes have died
            done = True
            '''
            with open('PPJresultsRL.txt', 'a', newline='') as f:
                f.write(str(self.PPJ) + ",")
                f.write(str(self.nrjList) + ",")
                f.write(str(self.dataList) + ",")
            '''


        if action == 0:  # This action is yPos -= 1
            if self.state[1] > 0:
                self.state[1] -= 1
                self.sinkSpeed = 1
                self.EE.updateEnv(0, -1, PR)

            else:
                reward = -50

        elif action == 1: # This action is yPos += 1
            if self.state[1] < ySize:
                self.state[1] += 1
                self.sinkSpeed = 1
                self.EE.updateEnv(0, 1, PR)
            else:
                reward = -50

        elif action == 2:  # This action is xPos += 1
            if self.state[0] < xSize:
                self.state[0] += 1
                self.sinkSpeed = 1
                self.EE.updateEnv(1, 0, PR)
            else:
                reward = -50

        elif action == 3:  # This action is xPos -= 1
            if self.state[0] > 0:
                self.state[0] -= 1
                self.sinkSpeed = 1
                self.EE.updateEnv(-1, 0, PR)
            else:
                reward = -50

        elif action == 4:  # This action is xPos -= 1 and yPos += 1
            if self.state[0] > 0 and self.state[1] < ySize:
                self.state[0] -= 1
                self.EE.updateEnv(-1, 1, PR)
                self.state[1] += 1
                self.sinkSpeed = math.sqrt(2) # sqrt(1^2 + 1^2)
                #self.EE.updateEnv(0, 1, PR)
            else:
                reward = -50

        elif action == 5:  # This action is xPos += 1 and yPos += 1
            if self.state[0] < xSize and self.state[1] < ySize:
                self.state[0] += 1
                self.EE.updateEnv(1, 1, PR)
                self.state[1] += 1
                self.sinkSpeed = math.sqrt(2) # sqrt(1^2 + 1^2)
                #self.EE.updateEnv(0, 1, PR)
            else:
                reward = -50

        elif action == 6:  # This action is xPos -= 1 and yPos -= 1
            if self.state[0] > 0 and self.state[1] > 0:
                self.state[0] -= 1
                self.EE.updateEnv(-1, -1, PR)
                self.state[1] -= 1
                self.sinkSpeed = math.sqrt(2) # sqrt(1^2 + 1^2)
                #self.EE.updateEnv(0, -1, PR)
            else:
                reward = -50

        elif action == 7:  # This action is xPos += 1 and yPos -= 1
            if self.state[0] < xSize and self.state[1] > 0:
                self.state[0] += 1
                self.EE.updateEnv(1, -1, PR)
                self.state[1] -= 1
                self.sinkSpeed = math.sqrt(2) # sqrt(1^2 + 1^2)
               #self.EE.updateEnv(0, -1, PR)
            else:
                reward = -50

        if not action in self.tempActList:
            act_temp = 0  # Variable used to get the corresponding action pair for every node
            for i in range(numNodes):
                if action == i + act_temp + 8:  # This action is PR += 1
                    if self.EE.nodes[i].PA < maxPR:
                        #reward += 5 # self.EE.nodes[i].PA
                        PR[i][1] += 1
                        self.state[2][i][1] = self.EE.nodes[i].PA + 1
                        self.EE.updateEnv(0, 0, PR)
                    else:
                        reward = -50
                    break  # Break from for-loop when the correct action is found

                elif action == i + act_temp + 9:  # This action is PR -= 1
                    if self.EE.nodes[i].PA > 0:
                        #reward -= 5 # 1/self.EE.nodes[i].PA
                        PR[i][1] -= 1
                        self.state[2][i][1] = self.EE.nodes[i].PA - 1
                        self.EE.updateEnv(0, 0, PR)
                    else:
                        reward = -50
                    break  # Break from for-loop when the correct action is found
                act_temp += 1

            i += 1
            speed_temp = 2
            step_temp = 0

            for j in range(3): # For different sink speeds
                if action == i + j + step_temp + act_temp + 8:  # This action is yPos -= 1
                    if self.state[1] > speed_temp-1:
                        self.state[1] -= speed_temp
                        self.sinkSpeed = speed_temp
                        self.EE.updateEnv(0, -speed_temp, PR)
                    else:
                        reward = -50

                elif action ==  i + j + step_temp + act_temp + 9:  # This action is yPos += 1
                    if self.state[1] < ySize-speed_temp+1:
                        self.state[1] += speed_temp
                        self.sinkSpeed = speed_temp
                        self.EE.updateEnv(0, speed_temp, PR)
                    else:
                        reward = -50

                elif  i + j + step_temp + act_temp + 10:  # This action is xPos += 1
                    if self.state[0] < xSize-speed_temp+1:
                        self.state[0] += speed_temp
                        self.sinkSpeed = speed_temp
                        self.EE.updateEnv(speed_temp, 0, PR)
                    else:
                        reward = -50

                elif action ==  i + j + step_temp + act_temp + 11:  # This action is xPos -= 1
                    if self.state[0] > speed_temp-1:
                        self.state[0] -= speed_temp
                        self.sinkSpeed = speed_temp
                        self.EE.updateEnv(-speed_temp, 0, PR)
                    else:
                        reward = -50

                elif action ==  i + j + step_temp + act_temp + 12:  # This action is xPos -= 1 and yPos += 1
                    if self.state[0] > speed_temp-1 and self.state[1] < ySize-speed_temp+1:
                        self.state[0] -= speed_temp
                        self.EE.updateEnv(-speed_temp, speed_temp, PR)
                        self.state[1] += speed_temp
                        self.sinkSpeed = math.sqrt(2*speed_temp) # sqrt(speed_temp^2+speed_temp^2)
                        # self.EE.updateEnv(0, 1, PR)
                    else:
                        reward = -50

                elif action ==  i + j + step_temp + act_temp + 13:  # This action is xPos += 1 and yPos += 1
                    if self.state[0] < xSize-speed_temp+1 and self.state[1] < ySize-speed_temp+1:
                        self.state[0] += speed_temp
                        self.EE.updateEnv(speed_temp, speed_temp, PR)
                        self.state[1] += speed_temp
                        self.sinkSpeed = math.sqrt(2*speed_temp) # sqrt(speed_temp^2+speed_temp^2)
                        # self.EE.updateEnv(0, 1, PR)
                    else:
                        reward = -50

                elif action ==  i + j + step_temp + act_temp + 14:  # This action is xPos -= 1 and yPos -= 1
                    if self.state[0] > speed_temp-1 and self.state[1] > speed_temp-1:
                        self.state[0] -= speed_temp
                        self.EE.updateEnv(-speed_temp, -speed_temp, PR)
                        self.state[1] -= speed_temp
                        self.sinkSpeed = math.sqrt(2*speed_temp) # sqrt(speed_temp^2+speed_temp^2)
                        # self.EE.updateEnv(0, -1, PR)
                    else:
                        reward = -50

                elif action ==  i + j + step_temp + act_temp + 15:  # This action is xPos += 1 and yPos -= 1
                    if self.state[0] < xSize-speed_temp+1 and self.state[1] > speed_temp-1:
                        self.state[0] += speed_temp
                        self.EE.updateEnv(speed_temp, -speed_temp, PR)
                        self.state[1] -= speed_temp
                        self.sinkSpeed = math.sqrt(2*speed_temp) # sqrt(speed_temp^2+speed_temp^2)
                    # self.EE.updateEnv(0, -1, PR)
                    else:
                        reward = -50
                step_temp += 7


        for i in range(numNodes):  # Change send status to True if node has sent during time segment
            if self.EE.nodes[i].PA > 0 and self.sendStatus == False:
                self.sendStatus[i] = True




        if self.timeSegTemp == time_segments - 1 and not all(self.sendStatus): # Ensure that all node sends 1 packet each round
            reward -= 1000
            for i in range(numNodes):
                if self.sendStatus[i] == False:
                    self.EE.nodes[i].PA = 1 # If node didn't send anything during a round, it now sends 1 packet

        for i in range(numNodes):
            #if self.EE.nodes[i].CHstatus == 1:  # If node is a CH
            dist = self.EE.nodes[i].getDistance(self.EE.sink)
            pacRate = self.EE.nodes[i].PA
            if dist >= max(xSize, ySize) / 2:
                reward -= 0.6 * dist
                reward += 1 * pacRate
            elif dist < max(xSize, ySize) / 2 and pacRate >= maxPR / 2:
                reward -= 3.4 * dist
                reward += 5 * pacRate
            elif dist < max(xSize, ySize) / 2 and pacRate < maxPR / 2:
                reward -= 2 * dist
                reward += 3 * pacRate
            # reward -= (self.EE.nodes[i].getDistance(self.EE.sink) * 400) # * 0.05)  # Reward for distance to each CH
            # reward += self.EE.nodes[i].energy * 0.05
            # reward += self.EE.nodes[i].PA * 0.01
        # reward += (self.EE.nodes[0].getEnergy() * 0.0001)

        # Increment WSN env
        # Substitute for communicate function in EnvironmentalEngine
        if self.timeSegTemp == time_segments - 1:  # Non CH sending at end of each round
            for i in range(len(self.EE.nodes)):
                if self.EE.nodes[i].alive:
                    if (self.EE.nodes[i].CHstatus == 0):
                        outcome = self.EE.nodes[i].sendMsg(self.EE.sink)
                        if not outcome:
                            print(f"Node {self.EE.nodes[i].ID} failed to send to node {self.EE.nodes[i].CHparent.ID}!\n")
                            actionmsg = self.EE.nodes[i].getActionMsg()
                            print(str(actionmsg) + "\n")

        for i in range(len(self.EE.nodes)):  # CH can send every time segment
            if self.EE.nodes[i].alive:
                if (self.EE.nodes[i].CHstatus == 1):
                    outcome = self.EE.nodes[i].sendMsg(self.EE.sink)
                    if not outcome:
                        print(f"Node {self.EE.nodes[i].ID} failed to send to node {self.EE.nodes[i].CHparent.ID}!\n")
                        actionmsg = self.EE.nodes[i].getActionMsg()
                        print(str(actionmsg) + "\n")

        self.timeSegTemp += 1


        return np.array(self.state), reward, done, {}

    def reset(self):
        '''
        Resets the entire WSN by placing the sink in a random position and all nodes have a random PR
        '''
        self.sendStatus = [False] * numNodes
        self.timeSegTemp = 0
        self.PPJ = []

        self.rndCounter = 0
        self.state = [random.randint(0, self.xSize), random.randint(0, self.ySize)]
        for i in range(numNodes):
            self.state.append([i, random.randint(0, maxPR)])  # CH status is appended below
            self.EE.nodes[i].energy =  maxNrj # random.random() * maxNrj
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
        self.state.append(self.sinkSpeed)


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
        self.EE.sink.xPos =  self.state[0]
        self.EE.sink.yPos =  self.state[1]
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
        plotEnv(self.EE, 3)

