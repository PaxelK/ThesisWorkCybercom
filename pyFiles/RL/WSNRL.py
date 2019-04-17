import gym
import gym_WSN
import random
import numpy as np

import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from plotEnv import *


'''
# Testing step method

ctrl.step(0)
ctrl.step(1)
ctrl.step(2)
ctrl.step(3)
ctrl.step(4)
ctrl.step(5)
'''

#print(a)
#ctrl.reset()
'''
class RLctrl():
    def __init__(self, n_episodes=1000, n_win_ticks=195, max_env_steps=None, gamma=0.6, epsilon=0.1, alpha=0.01,
                 batch_size=64, quiet=False):

        self.memory = deque(maxlen=100000)
        self.ctrl = gym.make('WSN-v0')
        self.gamma = gamma
        self.epsilon = epsilon
        self.alpha = alpha
        self.n_episodes = n_episodes
        self.n_win_ticks = n_win_ticks
        self.batch_size = batch_size
        self.quiet = quiet
        if max_env_steps is not None:
            self.env._max_episode_steps = max_env_steps

        # Init model
        self.model = Sequential()
        self.model.add(Dense(24, input_dim=6, activation='tanh'))
        self.model.add(Dense(48, activation='tanh'))
        self.model.add(Dense(2, activation='linear'))
        self.model.compile(loss='mse', optimizer=Adam(lr=self.alpha, decay=self.alpha_decay))



        def chooseAct(state):
            return self.ctrl.action_space.sample() if (np.random.random() <= epsilon) else np.argmax(self.model.predict(state))

        while True:
            self.ctrl.render()
            action = self.ctrl.action_space.sample()
            next_state, reward, done, _ = self.ctrl.step(action)
            # next_state = np.reshape(next_state, [1, 4])
            state = next_state


            '''

ctrl = gym.make('WSN-v0')


alpha = 0.1  # Learning rate of the model
gamma = 0.6  # Discount factor for q-values future in time
epsilon = 0.1  # Exploration rate for exploring the model

q_table = np.zeros([ctrl.observation_space.n, ctrl.action_space.n])

for i in range(100000):
    ctrl.reset()  # Reset environment to random position after each episode
    state = ctrl.s  # Variable for if episode is finished

    reward = 0  # Zero after each episode
    done = False

    while not done:

        action = np.argmax(q_table[int(state)])  # Chooses a random action

        next_state, reward, done, info = ctrl.step(action)

        # Update Q-table
        old_value = q_table[int(state), int(action)]  # Look up old q-value in Q-table
        next_max = np.max(q_table[int(next_state)])  # Get the max q-value given the chosen action

        # Update q-value for the state
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[int(state), int(action)] = new_value

        state = next_state

print("Training Finished")

done = False
# Run Q-learning after training by exploiting model to evaluate performance
ctrl.reset() # reset position of taxi to random location
state = ctrl.s  # Check current state after reset
while not done:
    ctrl.render()
    action = np.argmax(q_table[int(state)])  # Exploit learned values all the time
    next_state, reward, done, info = env.step(action)
    state = next_state


