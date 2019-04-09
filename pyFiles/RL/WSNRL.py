import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *
import numpy as np

class WSNRL:
    def __init__(self):

        PRamount = 4 # Amount of different PRs, e.g PRamount = 4 implies PR can be 0, 1, 2 or 3
        # Determine step size of mobile sink
        numRows = int(xSize/2)
        numCols = int(ySize/2)
        maxRow = numRows - 1
        maxCol = numCols - 1

        numStates =  int(numRows * numCols * numNodes * numNodes * PRamount)

        initialStateDist = np.zeros(numStates)
        numActions = 6
        P = {state: {action: []
                     for action in range(numActions)} for state in range(numStates)}

        for row in range(numRows):
            for col in range(numCols):
                for node in range(numNodes):
                    for PR in range(PRamount):  # +1 for being inside taxi
                        for action in range(numActions):
                            # Default values
                            new_row, new_col = row, col
                            reward = -1  # Default reward for moving sink
                            done = False  # Boolean for if episode is complete
                            sink_loc = (row, col)  # Position of sink

                            # Actions: 0 = Move south, 1 = Move north, 2 = Move east, 3 = Move west,
                            # 4 = Increase packet rate, 5 Decrease Packet rate
                            if action == 0:
                                newRow = min(row + 1, maxRow)
                            elif action == 1:
                                newRow = max(row - 1, 0)
                            if action == 2:
                                newCol = min(col + 1, maxCol)
                            elif action == 3:
                                newCol = max(col - 1, 0)
                            if action == 4:  # Increase PR of specific node
                                reward = 10
                            elif action == 5:  # Decrease PR of specific node
                                reward = -10

        print("Finished")



# Test WSNRL class
env = WSNRL()
'''
       
                        
                       
                           
        initial_state_distrib /= initial_state_distrib.sum()
        discrete.DiscreteEnv.__init__(
            self, num_states, num_actions, P, initial_state_distrib)

    def encode(self, taxi_row, taxi_col, pass_loc, dest_idx):
        # (5) 5, 5, 4
        i = taxi_row
        i *= 5
        i += taxi_col
        i *= 5
        i += pass_loc
        i *= 4
        i += dest_idx
        return i

    def decode(self, i):
        out = []
        out.append(i % 4)
        i = i // 4
        out.append(i % 5)
        i = i // 5
        out.append(i % 5)
        i = i // 5
        out.append(i)
        assert 0 <= i < 5
        return reversed(out)

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        out = self.desc.copy().tolist()
        out = [[c.decode('utf-8') for c in line] for line in out]
        taxi_row, taxi_col, pass_idx, dest_idx = self.decode(self.s)

        def ul(x):
            return "_" if x == " " else x

        if pass_idx < 4:
            out[1 + taxi_row][2 * taxi_col + 1] = utils.colorize(
                out[1 + taxi_row][2 * taxi_col + 1], 'yellow', highlight=True)
            pi, pj = self.locs[pass_idx]
            out[1 + pi][2 * pj + 1] = utils.colorize(out[1 + pi][2 * pj + 1], 'blue', bold=True)
        else:  # passenger in taxi
            out[1 + taxi_row][2 * taxi_col + 1] = utils.colorize(
                ul(out[1 + taxi_row][2 * taxi_col + 1]), 'green', highlight=True)

        di, dj = self.locs[dest_idx]
        out[1 + di][2 * dj + 1] = utils.colorize(out[1 + di][2 * dj + 1], 'magenta')
        outfile.write("\n".join(["".join(row) for row in out]) + "\n")
        if self.lastaction is not None:
            outfile.write("  ({})\n".format(["South", "North", "East", "West", "Pickup", "Dropoff"][self.lastaction]))
        else:
            outfile.write("\n")

        # No need to return anything for human
        if mode != 'human':
            with closing(outfile):
                return outfile.getvalue()
'''
