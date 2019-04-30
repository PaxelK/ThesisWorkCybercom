# import libraries
import gym  # Imports gym library from OpenAI
from IPython.display import clear_output  # Clears console display
from time import sleep
import numpy as np
import random   # Used for randomness in the exploration rate


# Brute force algorithm
def brute_force(env):
    epochs = 0  # Timesteps
    penalties, rewards = 0, 0

    frames = [] # For animations

    done = False  # bool for if one episode is completed

    while not done:
        action = env.action_space.sample() # Choose random action
        state, reward, done, info = env.step(action) # Update relevant information for q-learning

        # Count amount of incorrect pick-up and drop-off
        if reward == -10:
            penalties += 1

        # For animations
        frames.append({
            'frame': env.render(mode='ansi'),
            'state': state,
            'action': action,
            'reward': reward
        })

        epochs +=1

    print(f"Timesteps taken: {epochs}") # Print amount of iterations
    print(f"Penalties incurred: {penalties}")  # Print amount of penalties == -10
    return frames

# Q-learning algorithm
def q_learning(env):
    # Hyper parameters for the learning process
    alpha = 0.1  # Learning rate of the model
    gamma = 0.6  # Discount factor for q-values future in time
    epsilon = 0.1  # Exploration rate for exploring the model

    episodes = 1000  # Amount of episodes that the agent trains on

    #For displaying results
    all_epochs = []  # Time steps
    all_penalties =[]  # Penalties

    total_epochs, total_penalties = 0, 0

    # Init q-table with zeros. The size of the q-table is observation space (row) x action space (col)
    q_table = np.zeros([env.observation_space.n, env.action_space.n])

    for i in range(episodes): # for loop determines the amount of episodes (set in beginning of function)
        env.reset() # Reset environment to random position after each episode
        state = env.s  # Check current state after reset

        epochs, penalties, reward = 0, 0, 0   # Zero these parameters after each episode
        done = False # Variable for if episode is finished

        while not done: # Train the agent on an episode (done=True is set in the gym environment)
            if random.uniform(0,1) < epsilon:  # If the random value is smaller than epsilon, we explore the environment
                action = env.action_space.sample() # Chooses a random action
            else: # Otherwise exploit the model
                # Chooses action with largest value in Q-table for the current state. argmax() returns the index of the
                # highest value
                action = np.argmax(q_table[state])

            next_state, reward, done, info = env.step(action)  # Get relevant info for updating Q-table based on action

            # Update Q-table
            old_value = q_table[state, action] # Look up old q-value in Q-table
            next_max = np.max(q_table[next_state]) # Get the max q-value given the chosen action

            # Update q-value for the state
            new_value = (1 - alpha) * old_value + alpha *(reward + gamma * next_max)
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
    env.reset() # reset position of taxi to random location
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



def print_frames(frames):
    '''
    This function displays the taxi environment and depicts the actions that are taken by the agent
    :param frames: The frames from the brute_force or q_learning algorithm
    :return: None
    '''
    for i, frame in enumerate(frames):
        clear_output(wait=True)
        print(frame['frame'])
        print(f"Timestep: {i + 1}")
        print(f"State: {frame['state']}")
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        sleep(.1)




def main():
    '''
    Main function. Call this function to start program
    :return: None
    '''
    env = gym.make("Taxi-v2").env  # Create an instance of the environment (environment interface)
    state = env.encode(3, 1, 2, 0)  # (taxi row, taxi column, passenger index, destination index)
    env.s = 328  # Set initial state to state index
    # envs.s = state # Set current state to environment state
    # print("State:", state)  # Displays which state index the agent is in

    # envs.render() # Displays the environment in the console
    # print(envs.P[328]) # Prints the look-up/reward table

    # Brute Force
    #frames = brute_force(envs)

    # Q-learning
    frames = q_learning(env)

    print_frames(frames)

    '''
    print(f"Action Space: {envs.action_space}")  # Print size of Action Space
    print(f"State Space: {envs.observation_space}") # Print size of State Space
    '''


if __name__ == '__main__':
    main()
