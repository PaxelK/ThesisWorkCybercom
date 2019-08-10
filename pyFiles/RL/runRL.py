# -*- coding: utf-8 -*-
import time
import random
import math
import gym
import gym_WSN
import LEACHtest
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import csv
import nodePlacementGeneration  # Generates node placement and saves to csv file

import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *
from plotEnv import *
from EnvironmentEngineMPC import *

import matplotlib.pyplot as plt


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.8 #0.9    # discount rate
        self.epsilon_min = 0.05
        self.epsilon = 0.05 # exploration rate
        self.epsilon_decay = 0.9995
        self.learning_rate = 0.01
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        # Add layers to NN model
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(48, activation='relu'))
        #model.add(Dense(36, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        #model.compile(loss='mae', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  # Returns a random action in the action space
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # Returns the action that is predicted to yield the most reward

    def replay(self, batch_size):
        # Method to replay past experiences
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward

            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)
        self.model.compile(loss='mae', optimizer=Adam(lr=self.learning_rate))  # Compile NN


if __name__ == "__main__":
    env = gym.make('WSN-v0')
    state_size = env.observation_space.shape[0]  # Get amount of states (Number of states = 2 + 2*numNodes)
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)  # Create an instance of the agent

    '''
    # Uncomment if node placement needs to be hardcoded 
    env.EE.nodes[0].xPos = 130
    env.EE.nodes[0].yPos = 130

    env.EE.nodes[1].xPos = 170
    env.EE.nodes[1].yPos = 130

    env.EE.nodes[2].xPos = 130
    env.EE.nodes[2].yPos = 170

    env.EE.nodes[3].xPos = 170
    env.EE.nodes[3].yPos = 170

        
    env.EE.nodes[0].xPos = 250
    env.EE.nodes[0].yPos = 20

    env.EE.nodes[1].xPos = 250
    env.EE.nodes[1].yPos = 60

    env.EE.nodes[2].xPos = 210
    env.EE.nodes[2].yPos = 20

    env.EE.nodes[3].xPos = 210
    env.EE.nodes[3].yPos = 60
    '''

    TESTS = 10

    for tests in range(TESTS):
        nodePlacementGeneration.run()  # Generate new node placement for each test and save in csv file
        LEACHenv = LEACHtest.create()  # Create instance of LEACH environment
        LEACHenv.placeNodes()  # Place nodes according to node generation

        # Run WSN env with plotting after training
        agent.load("./save/wsn-dqn-speed.h5")  # Load weights of DQN from file
        avrRnd = []

        with open('nodePlacement.csv') as nodePlacement_file:  # Load the new node placement into DQN
            csv_reader = csv.reader(nodePlacement_file, delimiter=',')
            row_count = 0

            for row in csv_reader:
                i = 0
                rowVec = []

                for element in row:
                    rowVec.append(float(element))

                if row_count == 0:
                    for valueX in rowVec:
                        env.EE.nodes[i].xPos = valueX
                        i += 1
                if row_count == 1:
                    for valueY in rowVec:
                        env.EE.nodes[i].yPos = valueY
                        i += 1
                row_count += 1


        # Set default values
        done = False
        LEACHbool = False
        batch_size = 32
        rnd = 0
        state = env.reset()  # Reset env to a random state
        env.EE.sink.xPos = int(xSize / 2)
        env.EE.sink.yPos = int(ySize / 2)

        # Format state such that it can be used for training
        for i in range(2, numNodes + 2):
            state[i] = state[i][1]
        state[(2*numNodes)+2] = env.sinkSpeed
        state = np.reshape(state, [1, state_size])

        while not done or not LEACHbool:
            if len(env.EE.deadNodes) != numNodes:  # If RL environment is still alive
                rnd += 1
                action = agent.act(state)
                next_state_temp, reward, done, _ = env.step(action)


                # Format data for training
                next_state = [next_state_temp[0], next_state_temp[1]]
                for i in range(numNodes):
                    next_state.append(next_state_temp[2][i][1])
                for ii in range(numNodes):
                    next_state.append(next_state_temp[3][ii])
                next_state.append(env.sinkSpeed)
                next_state = np.array(next_state)
                next_state = np.reshape(next_state, [1, state_size])
                agent.remember(state, action, reward, next_state, done)
                state = next_state


            if len(LEACHenv.EE.deadNodes) != numNodes: # If LEACH environment is still alive
                LEACHbool = LEACHenv.step(env.CHtemp)


            if done or LEACHbool:  # Break when one environment is dead (or)
                print(f"Test: {tests+1}/{TESTS}")
                print("-------------LEACH Results-------------")
                print(f"Rounds survived: {LEACHenv.EE.rnd}")
                print(f"Data packets received: {LEACHenv.EE.sink.dataRec / 1000}")
                energyList = []
                for i in range(numNodes):
                    energyList.append(LEACHenv.EE.nodes[i].getEC())
                print(f"Energy consumed: {sum(energyList)}")

                # Uncomment if results shall be saved

                with open('LEACHresults.txt', 'a', newline='') as f:
                    f.write(str(LEACHenv.EE.rnd) + ",")
                    f.write(str(LEACHenv.EE.sink.dataRec / 1000) + ",")
                    f.write(str(sum(energyList)) + ",")



                print("--------------DQN Results--------------")
                print(f"Rounds survived: {env.EE.rnd}")
                print(f"Data Packets Received Sink: {env.EE.sink.dataRec / 1000}")
                energyListDQN = []
                for i in range(numNodes):
                    energyListDQN.append(env.EE.nodes[i].getEC())
                print(f"Energy consumed: {sum(energyListDQN)}")

                # Uncomment if results shall be saved

                with open('RLresults.txt', 'a', newline='') as fDQN:
                    fDQN.write(str(env.EE.rnd) + ",")
                    fDQN.write(str(env.EE.sink.dataRec / 1000) + ",")
                    fDQN.write(str(sum(energyListDQN)) + ",")

                break

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

            #env.render()


        #avrRnd.append(rnd)

    #print(f"avrRnd: {avrRnd}")
    #print(f"Mean Rounds: {sum(avrRnd) / len(avrRnd)}")
