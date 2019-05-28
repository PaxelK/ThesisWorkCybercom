import math

'''
This function sets all the parameters that are needed in the simulation 
'''
### Bleach Parameters

f = 1.5   # Weight coefficient between old LEACH and new SoC term. For regular Leach, set f>1
k = 4000  # Size of data package, units in bits
p = 0.1  # Suggested percentage of cluster head, a 5 percent of the total amount of nodes used in the network is proposed to give good results

########################### Network Establishment Parameters ###############################
### Area of Operation ###
# Field Dimensions in meters #
xSize = 100
ySize = 100
x = 0  # Added for better display results of the plot
y = 0  # Added for better display results of the plot

numNodes = 50  # Number of Nodes in the field
dead_nodes = 0 # Number of Dead Nodes in the beginning

#### Data Packet Info ###
ps = 1000
maxPR = 20				# Maximum amount of packages that can be sent during one transmission round

### Energy Values ###
energyMode = "rand"  	# Energy mode can be "rand"=random or "distr"=distributed
maxNrj = 0.5
Eelec = 50*10**(-9)   	# Energy required to run circuity (both for transmitter and receiver), units in Joules/bit
ETx = 50*10**(-9)     	# Units in Joules/bit
ERx = 50*10**(-9)     	# Units in Joules/bit
Eamp = 100*10**(-12)  	# Transmit Amplifier Types, units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
EDA = 5*10**(-9)      	# Data Aggregation Energy, units in Joules/bit
nrjGenFac = 0.1      	# Energy factor for generated energy

plotlen = 10            # Amount of rounds that are plotted at the same time


time_segments = 10      # Amount of time segments per transmission round