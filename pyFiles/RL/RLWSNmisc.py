import sys

sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *
import numpy as np
from random import *

'''
class WSNRL:
    def __init__(self, nodesList=np.zeros(numNodes)):

        self.PRamount = 4  # Amount of different PRs, e.g PRamount = 4 implies PR can be 0, 1, 2 or 3
        self.actionSpace = 6

        # Determine a step size of mobile sink
        self.numRows = int(xSize / 2)
        self.numCols = int(ySize / 2)
        maxRow = self.numRows - 1
        maxCol = self.numCols - 1

        numStates = int(self.numRows * self.numCols * numNodes * (numNodes * self.PRamount))

        # initialStateDist = np.zeros(numStates)

        P = {state: {action: []
                     for action in range(self.actionSpace)} for state in range(numStates)}

        for row in range(self.numRows):
            for col in range(self.numCols):
                for node in range(numNodes):
                    # for PRa in range(PRamount):
                    for action in range(self.actionSpace):
                        # Default values
                        state = self.encode(row, col, node)
                        for nodeObj in nodesList:
                            if nodeObj.CHstatus == 1:
                                pass

                        newRow, newCol, newPacketRates = row, col, packetRates
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
                            packetRates[node] = min(self.PRamount - 1, packetRates[node] + 1)  # PR can be zero
                            reward = 10
                        elif action == 5:  # Decrease PR of specific node
                            packetRates[node] = max(0, packetRates[node] - 1)
                            reward = -10

                        newState = self.encode(newRow, newCol, packetRates)
                        P[state][action].append((1.0, newState, reward, done))

        print("Finished")

    def encode(self, sinkRow, sinkCol, packetRates):
        # (numRow) numCols, numNodes
        i = sinkRow
        i *= self.numCols
        i += sinkCol
        i *= self.PRamount * numNodes
        i += packetRates
        return i

    def decode(self, i):
        out = []
        out.append(i % self.PRamount * numNodes)
        i = i // self.PRamount * numNodes
        out.append(i % self.numCols)
        i = i // self.numCols
        out.append(i)
        assert 0 <= i < self.numRows
        return reversed(out)

    def q_learning(self):
        # Init q-table with xeros. The size of the q-table is observation space (row) X action space (col)
        q_table = np.zeros([env.observation_space.n, env.action_space.n])

        for i in range(1, episodes + 1):  # for loop determines the amount of episodes (set in beginning of function)
            env.reset()  # Reset environment to random position after each episode
            state = env.s  # Check current state after reset

            epochs, penalties, reward = 0, 0, 0  # Zero these parameters after each episode
            done = False  # Variable for if episode is finished

            while not done:  # Train the agent on an episode (done=True is set in the gym environment)
                if random.uniform(0,
                                  1) < epsilon:  # If the random value is smaller than epsilon, we explore the environment
                    action = env.action_space.sample()  # Chooses a random action
                else:  # Otherwise exploit the model
                    # Chooses action with largest value in Q-table for the current state. argmax() returns the index of the
                    # highest value
                    action = np.argmax(q_table[state])

                next_state, reward, done, info = env.step(
                    action)  # Get relevant info for updating Q-table based on action

                # Update Q-table
                old_value = q_table[state, action]  # Look up old q-value in Q-table
                next_max = np.max(q_table[next_state])  # Get the max q-value given the chosen action

                # Update q-value for the state
                new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
                q_table[state, action] = new_value

                # For plotting amount of -10 rewards
                if reward == -10:
                    penalties += -1
                    total_penalties += -1

                # Update state, increment/append plotting parameters
                state = next_state
                epochs += 1
                total_epochs += 1
                all_penalties.append(penalties)
                all_epochs.append(epochs)

            # Prints amount of episodes trained
            if i % 10000 == 0:
                clear_output(wait=True)
                print(f"Episode: {i}")

        print("Training finished \n")

        # Evaluate performance of Q-learning algorithm
        print(f"Amount of penalties: {total_penalties}")

        print(f"Results after {episodes} episodes:")
        print(f"Average timesteps per episode: {total_epochs / episodes}")
        print(f"Average penalties per episode: {total_penalties / episodes}")

        # Animating taxi after learning
        frames = []
        epochs = 0

        done = False

        # Run Q-learning by exploiting model to evaluate performance
        env.reset()  # reset position of taxi to random location
        state = env.s  # Check current state after reset
        while not done:
            action = np.argmax(q_table[state])  # Exploit learned values all the time
            next_state, reward, done, info = env.step(action)
            state = next_state

            epochs += 1
            frames.append({
                'frame': env.render(mode='ansi'),
                'state': state,
                'action': action,
                'reward': reward})

        print(f"Q-learning rounds: {epochs}")
        return frames


# Test WSNRL class
env = WSNRL()

'''


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
        self.state = EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        for i in range(numNodes):
            self.state.append(EE.nodes[i].PA)

        self.steps_beyond_done = None

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

        print(self.state)
        print("---------------------")
        return np.array(self.state), reward, done, {}

    def reset(self):
        '''
        Resets the entire WSN by placing the sink in a random position and all nodes have a random PR
        '''
        self.state = [random.randint(0, self.xSize), random.randint(0, self.ySize)]
        for i in range(numNodes):
            self.state.append([i, random.randint(0, self.PRamount - 1)])
        return np.array(self.state)

    def render(self, mode='human'):
        plotEnv(EE)

