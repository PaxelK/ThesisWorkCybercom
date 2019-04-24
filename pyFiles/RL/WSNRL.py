import math
import gym
import gym_WSN
import random
import numpy as np

import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *
from plotEnv import *
from EnvironmentEngine import *

class RLctrl():
    def __init__(self):
        self.env = gym.make('WSN-v0')

        self.buckets = (1, 1, 1)  # Down-scaling feature space to discretize range
        self.n_episodes = 1000  # Number of training episodes
        self.alpha = 0.1  # Learning rate
        self.epsilon = 0.1  # Exploration rate
        self.gamma = 0.6  # Discount factor
        self.ada_divisor = 25  # Used to decay learning parameters

        max_env_steps = None  # Maximum amount of steps in an episode
        if max_env_steps is not None:
            self.env._max_episode_steps = max_env_steps

        self.Q = np.zeros(self.buckets + (self.env.action_space.n,))

    def discretize(self, obs):
        # Needs to be updated to handle more than one node
        upper_bounds = [self.env.observation_space.high[0], self.env.observation_space.high[1], self.env.observation_space.high[2]]
        lower_bounds = [self.env.observation_space.low[0], self.env.observation_space.low[1], self.env.observation_space.low[2]]
        ratios = [(obs[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(len(obs)-1)]
        ratios.append((obs[2][1] + abs(lower_bounds[2])) / (upper_bounds[2] - lower_bounds[2]))
        new_obs = [int(round((self.buckets[i] - 1) * ratios[i])) for i in range(len(obs))]
        new_obs = [min(self.buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
        return tuple(new_obs)

    def choose_action(self, state, epsilon):
        if (np.random.random() <= epsilon):
            return self.env.action_space.sample()
        else:
            return np.argmax(self.Q[state])

    def update_q(self, state_old, action, reward, state_new, alpha):
        self.Q[state_old][action] += alpha * (reward + self.gamma * np.max(self.Q[state_new]) - self.Q[state_old][action])

    def run(self):

        for i in range(self.n_episodes):
            current_state = self.discretize(self.env.reset())
            done = False

            while not done:
                #self.env.render()
                action = self.choose_action(current_state, self.epsilon)
                obs, reward, done, _ = self.env.step(action)
                new_state = self.discretize(obs)
                self.update_q(current_state, action, reward, new_state, self.alpha)
                current_state = new_state
            print(f"i = {i}")




if __name__ == "__main__":
    solver = RLctrl()
    solver.run()








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



'''
# From  when using discrete env
alpha = 0.1  # Learning rate of the model
gamma = 0.6  # Discount factor for q-values future in time
epsilon = 0.1  # Exploration rate for exploring the model

episodes = 10000  # Amount of episodes that the agent trains on

q_table = np.zeros([ctrl.observation_space.n, ctrl.action_space.n])  # Init q_table to all zeros

for i in range(episodes):
    print(f"Episode: {i}")
    ctrl.reset()  # Reset environment to random position after each episode
    state = ctrl.s  # Variable for if episode is finished

    # Set variables to default values after each episode
    reward = 0  # Zero reward after each episode
    done = False  # Boolean for if episode has finished

    times = 0  # Debugging variable, counter for amount of rounds in episode
    while not done:
        times += 1

        #action = np.argmax(q_table[int(state)])  # Chooses action with greatest q-value
        action = ctrl.action_space.sample()  # Chooses random action in action space

        # Debugging prints
        if times == 7402:
            print(f"action: {action}")
        #print(times)

        next_state, reward, done, info = ctrl.step(action)  # Take the selected action and update variables

        # Update Q-table
        old_value = q_table[state, action]  # Look up old q-value in Q-table
        next_max = np.max(q_table[next_state])  # Get the max q-value given the chosen action

        # Update q-value for the state
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        # Hard coded for one node (Needs to be extended later)
        if action == 0:
            ctrl.EE.updateEnv(0, -ctrl.numRows, [[0, ctrl.EE.nodes[0].PA]])
        elif action == 1:
            ctrl.EE.updateEnv(0, ctrl.numRows, [[0, ctrl.EE.nodes[0].PA]])
        elif action == 2:
            ctrl.EE.updateEnv(ctrl.numCols, 0, [[0, ctrl.EE.nodes[0].PA]])
        elif action == 3:
            ctrl.EE.updateEnv(-ctrl.numCols, 0, [[0, ctrl.EE.nodes[0].PA]])
        elif action == 4:
            ctrl.EE.updateEnv(0, 0, [[0, ctrl.EE.nodes[0].PA]])
        elif action == 5:
            ctrl.EE.updateEnv(0, 0, [[0, ctrl.EE.nodes[0].PA]])

        ctrl.EE.cluster()
        ctrl.EE.communicate()
        ctrl.EE.iterateRound()

        state = int(next_state)

print("Training Finished")
'''

'''
done = False
# Run Q-learning after training by exploiting model to evaluate performance
ctrl.reset() # reset position of taxi to random location
state = ctrl.s  # Check current state after reset
while not done:
    ctrl.render()
    action = np.argmax(q_table[int(state)])  # Exploit learned values all the time
    next_state, reward, done, info = ctrl.step(action)
    state = next_state

'''
