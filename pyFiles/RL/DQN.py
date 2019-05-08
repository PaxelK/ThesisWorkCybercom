# -*- coding: utf-8 -*-
import random
import math
import gym
import gym_WSN
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *
from plotEnv import *
from EnvironmentEngine import *

import matplotlib.pyplot as plt


EPISODES = 20

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(36, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
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

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
    env = gym.make('WSN-v0')
    state_size = env.observation_space.shape[0]  # Get amount of states (3 states with 1 node)
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)  # Create an instance of the agent
    # agent.load("./save/wsn-dqn.h5")
    # Set default values
    done = False
    batch_size = 32

    avrRnd = []
    # Train agent
    for e in range(EPISODES):
        done = False
        rnd = 0
        state = env.reset()  # Reset env to a random state
        # Format state such that it can be used for training
        state[2] = state[2][1]
        state = np.reshape(state, [1, state_size])
        while not done:
            rnd += 1
            # env.render()
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            #reward = reward if not done else -10
            next_state[2] = next_state[2][1]
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            #print(next_state[0])


            if done:
                print(f"episode: {e}/{EPISODES}, e: {agent.epsilon}, rnd: {rnd} \n")
                break

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

        avrRnd.append(rnd)
        # if e % 10 == 0:  # Save weights for every 10th episode
        #     agent.save("./save/wsn-dqn.h5")

    print(f"avrRnd: {avrRnd}")

    x = np.linspace(0, len(avrRnd), num=len(avrRnd), endpoint=True)
    plt.plot(x, avrRnd)
    plt.show()


    done = False
    rnd = 0
    state = env.reset()  # Reset env to a random state
    # Format state such that it can be used for training
    state[2] = state[2][1]
    state = np.reshape(state, [1, state_size])
    while not done:
        env.render()
        rnd += 1
        # env.render()
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        # reward = reward if not done else -10
        next_state[2] = next_state[2][1]
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        # print(next_state[0])
