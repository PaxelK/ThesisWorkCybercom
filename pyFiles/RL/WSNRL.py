import sys
sys.path.append("..")  # Adds higher directory to python modules path.
import gym
import gym_WSN
import random
import numpy as np

from plotEnv import *

ctrl = gym.make('WSN-v0') # Initiate RL environment
ctrl.step(0)
ctrl.step(1)
ctrl.step(2)
ctrl.step(3)
ctrl.step(4)
ctrl.step(5)



#print(a)
#ctrl.reset()
while True:
    ctrl.render()
    action = ctrl.action_space.sample()
    next_state, reward, done, _ = ctrl.step(action)
    #next_state = np.reshape(next_state, [1, 4])
    state = next_state


    '''
    next_state, reward, done, info = env.step(action)

    old_value = q_table[state, action]
    next_max = np.max(q_table[next_state])

    # Update the new value
    new_value = (1 - alpha) * old_value + alpha * \
                (reward + gamma * next_max)
    q_table[state, action] = new_value

    if reward == -10:
        penalties += 1

    state = next_state
    epochs += 1
    '''


