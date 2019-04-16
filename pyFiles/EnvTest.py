from EnvironmentEngine import *
from plotEnv import *

EE = EnvironmentEngine()  # Initiate environment

x, y = EE.sink.getPos()  # Get position/coordinates of sink





# Get PR for all nodes (PR should be zero for dead nodes)
PRcontrl = []
for i in range(numNodes):
    PRcontrl.append([i, 10])  # [Node ID, PR of node]


'''
EE.updateEnv(20, 43, PRcontrl)  # [sinkx, sinky, PRlist]
x, y = EE.sink.getPos()
print(f"x = {x},  y = {y} \n")



print("----------------------------------------")
for i in range(numNodes):
    print(EE.nodes[i].PA)

EE.updateEnv(-120, 30, PRcontrl)  # [sinkx, sinky, PRlist]
x, y = EE.sink.getPos()
print(f"x = {x},  y = {y} \n")
print("----------------------------------------")
EE.updateEnv(305, 660, PRcontrl)  # [sinkx, sinky, PRlist]
x, y = EE.sink.getPos()
print(f"x = {x},  y = {y} \n")
print("----------------------------------------")

EE.updateEnv(-1000, -1000, PRcontrl)
x, y, d = EE.sinkStatus()
print(f"x = {x},  y = {y}, dataRecieved = {d} \n")
print("----------------------------------------")
EE.updateEnv(20, 20, PRcontrl)
x, y, d = EE.sinkStatus()
print(f"x = {x},  y = {y}, dataRecieved = {d} \n")
print("----------------------------------------")



states = EE.getStates()
'''
while True:  # Run until all node dies
    print(f"Round = {EE.rnd}")
    
    #print(f"plotRnd Length = {len(EE.plotRnd)}")
    #print(f"meanEClist Length = {len(EE.meanEClist)}")
    #print(f"EClist Length = {len(EE.EClist)}")
    #print(f"PackReclist Length = {len(EE.PackReclist)}")
    #print(f"deadnodes Length = {len(EE.deadNodes)}")
    
    plotEnv(EE)

    EE.updateEnv(1, 1, PRcontrl)
    EE.cluster()
    EE.communicate()
    EE.iterateRound()



    if len(EE.deadNodes) == numNodes: # Break when all nodes have died
        break

'''
# Testing of classes starts here 
sink = Sink(100, 100)  # Creates an instance of the sink (sizex, sizey)


nodeList = []
if energyMode == "rand":
    for i in range(0, numNodes):
        nodeList.append(Node(i, random()*xSize, random()*ySize, maxNrj*random()))
elif energyMode == "distr":
    for i in range(0, numNodes):
        nodeList.append(Node(i, random()*xSize, random()*ySize, maxNrj))
else:
    print("The choice of energy mode is invalid! \n")


for ii in range(0, n-1):
    print(nodeList[ii].energy)
    
# Test to move sink position
sink.move(-600, 54)
print(sink.xPos)
print(sink.yPos)
print('------------------------')
sink.move(10, -90)
print(sink.xPos)
print(sink.yPos)


# Testing energy generated
print(f"Energy: {nodeList[5].energy}")
print(f"SoC: {nodeList[5].SoC}\n")
nodeList[5].generateNRJ()
print(f"Energy: {nodeList[5].energy}")
print(f"SoC: {nodeList[5].SoC}\n")
nodeList[5].generateNRJ()
print(f"Energy: {nodeList[5].energy}")
print(f"SoC: {nodeList[5].SoC}\n")
nodeList[5].generateNRJ()


# Testing generating CH status and clearing CH status

CHamount = 0  # Amount of CH

for i in range(0, n):  # Hard coded for the amount of nodes
    nodeList[i].generateCHstatus(0.9, 0.05, 0) # (f, p, rnd)
    if nodeList[i].CHstatus == 1:
         CHamount += 1  # Increments the CH counter

print(f"Amount of CH after connection: {CHamount}")

CHamount = 0
for i in range(0, n):  # Hard coded for the amount of nodes
    nodeList[i].clearConnection()  # Try to clear CH status
    if not nodeList[i].CHparent == []:
         CHamount = CHamount + 1  # Increments the CH counter

print(f"Amount of CH after clearing connection: {CHamount}")

# Test getdistance methos

print(nodeList[5].xPos)
print(nodeList[5].yPos)
print('----------------------------')
print(nodeList[6].xPos)
print(nodeList[6].yPos)
print('----------------------------')
print(f"Distance from node 5 to 6: {nodeList[5].getDistance(nodeList[6])}")
print(f"Distance from node 6 to 5: {nodeList[6].getDistance(nodeList[5])}")


# Test updateEnergy and correctEnergy method

while nodeList[4].alive:
    print("-------------------------------------------------------------------------")
    print(f"Energy: {nodeList[4].energy}")
    print(f"Energy consumed: {nodeList[4].nrjCons}")
    print(f"State of Charge: {nodeList[4].SoC}")
    print(f"Alive: {nodeList[4].alive}")
    energyCons = 0.1  # Amount of energy consumed
    nodeList[4].updateEnergy(energyCons)  # Assume that node 4 consumes energy
    print("------------------------Before correctEnergy-----------------------------")
    print(f"Energy: {nodeList[4].energy}")
    print(f"Energy consumed: {nodeList[4].nrjCons}")
    print(f"State of Charge: {nodeList[4].SoC}")
    print(f"Alive: {nodeList[4].alive}")

    if nodeList[4].energy < 0:
        nodeList[4].correctEnergy()


print("-----------------------After CorrectEnergy-------------------------------")
print(f"Energy: {nodeList[4].energy}")
print(f"Energy consumed: {nodeList[4].nrjCons}")
print(f"State of Charge: {nodeList[4].SoC}")
print(f"Alive: {nodeList[4].alive}")


# Testing sendMsg
nodeList[6].CHstatus = 1
nodeList[4].connect(nodeList[6])
nodeList[4].sendMsg(sink)
print(nodeList[4].actionMsg)
'''

