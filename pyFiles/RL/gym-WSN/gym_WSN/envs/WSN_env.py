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
            int(self.xSize / 50),
            int(self.ySize / 50),
            4])

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

        self.steps_beyond_done = None

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

        # Default values
        reward = 0
        done = False

        if len(self.EE.deadNodes) == numNodes:
            done = True

        if action == 0:
            self.state[1] -= 1  # yPos -
            self.EE.updateEnv(0, -1, PR)


        elif action == 1:
            self.state[1] += 1  # yPos +
            self.EE.updateEnv(0, 1, PR)

        elif action == 2:
            self.state[0] += 1  # xPos +
            self.EE.updateEnv(1, 0, PR)

        elif action == 3:
            self.state[0] -= 1  # xPos -
            self.EE.updateEnv(-1, 0, PR)

        # PR is hard coded for one node
        elif action == 4:
            reward = 10
            self.EE.nodes[0].PA = min(self.PRamount - 1, self.EE.nodes[0].PA + 1)
            self.state[2][1] = self.EE.nodes[0].PA  # PR +
            self.EE.updateEnv(0, 0, PR)

        elif action == 5:
            reward = -10
            self.EE.nodes[0].PA = max(0, self.EE.nodes[0].PA - 1)
            self.state[2][1] = self.EE.nodes[0].PA  # PR -
            self.EE.updateEnv(0, 0, PR)

        self.EE.cluster()
        self.EE.communicate()
        self.EE.iterateRound()

        print(self.state)
        print("---------------------")
        return np.array(self.state), reward, done, {}

    def reset(self):
        '''
        Resets the entire WSN by placing the sink in a random position and all nodes have a random PR

        TODO: Reset the environment parameters as well, eg. packets sent, energy consumed etc.
        '''
        self.state = [random.randint(0, self.xSize), random.randint(0, self.ySize)]
        for i in range(numNodes):
            self.state.append([i, random.randint(0, self.PRamount - 1)])
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

