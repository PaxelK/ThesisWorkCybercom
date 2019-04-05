# Import libraries
import gym
import numpy as np
import random
from IPython.display import clear_output

# Init/make Taxi-V2 Env
env = gym.make("Taxi-v2").env

# Init q-table with xeros. The size of the q-table is observation space (row) X action space (col)
q_table = np.zeros([env.observation_space.n, env.action_space.n])

# Hyper parameters for the learning process
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor for q-values future in time
epsilon = 0.1  # Exploration rate for exploring the model


for i in range(1, 100001):
    state = env.reset()

    # Init Vars
    epochs, penalties, reward, = 0, 0, 0
    done = False

    while not done:
        env.render
        if random.uniform(0, 1) < epsilon:
            # Check the action space
            action = env.action_space.sample()
        else:
            # Check the learned values
            action = np.argmax(q_table[state])

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


    if i % 100 == 0:
        clear_output(wait=True)
        print(f"Episode: {i}")

env.render()
print("Training finished.")
