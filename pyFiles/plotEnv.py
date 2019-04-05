import matplotlib.pyplot as plt
import numpy as np


def plotEnv(env):
    '''
    This function plots the WSN system
    :param env: Environment engine which contains the nodes and sink
    '''
    # Plotting Simulation Results "Operating Nodes per Round"
    nodePos = env.posNodes
    xs, ys = env.sink.getPos()
    ECsum, ECstats = env.getECstats()
    PRsum, PRstats = env.getPRstats()
    meanEC = env.getECmeanStats()
    ndead, deadNodes = env.getDeadNodes()


    # Create figure 1
    plt.figure(1)
    plt.clf()
    plt.plot(nodePos[:, 0], nodePos[:, 1],  'ro', markersize = 8)
    plt.plot(xs, ys, marker='o', markersize = 16, markerfacecolor= 'g')


    # Create figure 2
    plt.figure(2)
    plt.clf()
    # Create sub-plot
    plt.subplot(133)
    # Create plot
    plt.plot(env.plotRnd, ECstats, linewidth=2, Color='r')
    # Create x-label
    plt.xlabel("Round", fontsize =11)
    # Create y-label
    plt.ylabel("Sum of energy", fontsize =11)
    # Create title
    plt.title("Sum of EC vs. round", fontsize =14)

    # Create sub-plot
    subplot2 = plt.subplot(131)
    # Create plot
    plt.plot(env.plotRnd, PRstats, linewidth = 2, color = 'g')
    # Create x-label
    plt.xlabel("Round", fontsize =11)
    # Create y-label
    plt.ylabel("Sum of bits sent to sink", fontsize =11)
    # Create title
    plt.title("Number of packet sent to BS vs. round", fontsize =14)

    # Create sub-plot
    subplot3 = plt.subplot(132)
    # Create plot
    # print(f"Number of dead nodes = {ndead}")
    plt.plot(env.rnd, ndead, linewidth = 2, color = 'b')
    # Create x-label
    plt.xlabel("Round", fontsize =11)
    # Create y-label
    plt.ylabel("# of dead nodes", fontsize =11)
    # Create title
    plt.title("Number of dead node vs. round", fontsize =14)

    plt.show(block=False)
    plt.pause(0.2)