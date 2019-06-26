import matplotlib.pyplot as plt
import numpy as np
from setParams import *
import pylab as pl
import math

def plotEnv(env, figNr):
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
    ndead, deadNodes, plotDeadNodes = env.getDeadNodes()


    # Create figure 1
    if(figNr==1 or figNr==3):
        plt.figure(1)
        plt.clf()
        for n in env.nodes:
            if n.CHstatus is 1:
                    plt.plot(n.xPos, n.yPos, 'bo')  # plot x and y using blue circle markers
                    pl.text(n.xPos, n.yPos, str(n.ID), color="teal", fontsize=10)
            else:
                if(n.CHparent.ID != math.pi):
                    plt.plot(n.xPos, n.yPos, 'go')  # plot x and y using blue circle markers
                else:
                    plt.plot(n.xPos, n.yPos, 'yo')
        
        #plt.plot(nodePos[:, 0], nodePos[:, 1],  'ro', markersize = 6)
        plt.plot(xs, ys, marker='o', markersize = 12, markerfacecolor= 'r')
        plt.xlim(0, xSize)
        plt.ylim(0, ySize)

    # Create figure 2
    if(figNr == 2 or figNr == 3):
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
        plt.plot(env.plotRnd, plotDeadNodes, linewidth = 2, color = 'b')
        # Create x-label
        plt.xlabel("Round", fontsize =11)
        # Create y-label
        plt.ylabel("# of dead nodes", fontsize =11)
        # Create title
        plt.title("Number of dead node vs. round", fontsize =14)
    
        plt.show(block=False)
    plt.pause(0.1)
