import math  # Needed for sqrt
import random
import setParams as sP
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl


class Node:
    def __init__(self, id, x, y, nrj):
        '''
        Constructor: takes in arguments for id, position, size of packages
        that get sent during transmission, starting energy level of node,
        maximum amount of energy that can be stored by the node
        (which also lead to the current state of charge of the node)

        Initial amount of packets sent during each transmission is set to
        1, cluster head status is set to 0 = NOT CLUSTER HEAD.
        If node starts of with energy it is seen as alive.

        :param id: ID of node
        :param x: Position in x for node
        :param y: Position in y for node
        :param nrj: Amount of initaial energy in node
        '''
        self.ID = id                           # ID of node
        self.xPos = x                          # x and y position of node
        self.yPos = y
        self.pSize = sP.ps                        # Preset packet size of each message
        self.PA = 1                            # Packet amount = amount of packets sent each transmission round
        self.energy = nrj                      # Create amount of energy [J] residing in node
        self.maxEnergy = sP.maxNrj                  # Max amount of energy [J] that can be stored in node
        self.SoC = self.energy / self.maxEnergy  # State of charge = Percentage of charge in node
        self.CHstatus = 0                      # Cluster head status: 1 if CH, 0 if not CH
        self.CHparent = None                   # Reference to the nodes current cluster head
        self.dataRec = 0                       # Data received = amount of data the node has received
        self.PS = 0                            # Packages sent = amount of packages the node has sent
        self.nrjCons = 0                       # Energy consumed [J] = Amount of energy the node has consumed
        self.actionMsg = ''                    # String containing message about connection and sending status
        self.CHflag = 0                        # Determines if node has been CH during a LEACH episode
        self.conChildren = 0                   # Number of connected children.
        self.tempDataRec = 0                   # Temporary held data that are then going to the sink.
        self.maxPR = sP.maxPR                  # Maximum amount of packets that can be sent during a transmission round
        if self.energy > 0:
            self.alive = True                  # Boolean for if node is alive
        else:
            self.alive = False


        self.otherBLEACH = False
        self.spread = 0.5
        """
        Creates the lookup table for the alternative BLEACH
        """
        self.tLookUp = []
        for i in range(0,int(1/sP.p)):
            self.tLookUp.append((sP.p / (1 - sP.p * (i % (1 / sP.p)))))
        
        
        self.maxVec = (1+self.spread)*np.array(self.tLookUp);
        self.minVec = (1-self.spread)*np.array(self.tLookUp);
                
        self.tVector = []
        for i in np.linspace(-self.spread,self.spread,100):
            self.tVector.append(np.array(self.tLookUp)*(1+i))
        
    def getDataRec(self):
        return self.dataRec

    def getPS(self):
        return self.PS

    def getEC(self):
        return self.nrjCons

    def getPA(self):
        return self.PA

    def getPos(self):
        x = self.xPos
        y = self.yPos
        return x, y

    def getActionMsg(self):
        '''
        Gets the action message. Mainly for debugging purposes.
        :return: Action message
        '''
        return self.actionMsg

    def getCHstatus(self):
        '''
        Method gets the CH status, i.e. if the node is a cluster head.
        :return: CHstatus = 1 if CH, else 0
        '''
        return self.CHstatus

    def getDistance(self, node):
        '''
        :param node: Node object of the node that the distance is measured between
        :return: distance between this node and an arbitrary node.
        '''
        distance = math.sqrt((self.xPos - node.xPos)**2 + (self.yPos - node.yPos)**2)
        return distance

    def getEnergy(self):
        '''
        Gets the amount of energy stored in a node
        :return: getEnergy = amount of energy in node
        '''
        return self.energy

    def clearTempDataRec(self):
        '''
        Clears the temporary data received as a CH from child nodes during transmission round
        '''
        self.tempDataRec = 0
    
    def clearConnection(self):
        '''
        Sets the CHparent variable to null
        '''
        self.CHparent = []

    def incrementConChildren(self):
        '''
        Increments the number of connected "children" to this node
        '''
        self.conChildren += 1
        
    def resetConChildren(self):
        '''
        Resets the number of connected "children" to this node
        '''
        self.conChildren = 0

    def connect(self, node):
        '''
        Connection here adds another node object as a CH reference to
        this object and is stored in CHparent. If the connection is a success, the number of connected children
        for the parent node is incremented with "incrementConChildren()". If the connection fails
        due to the target node being dead, or not being a CH, or if this
        node is already a CH, an error message is printed out.
        :param node: Node that connection is established with
        '''
        if node.alive:
            self.CHparent = node
            self.actionMsg = "Node " + str(self.ID) + " of type " + str(self.CHstatus) +\
                             " connected successfully to target node " + str(node.ID) + " of type " +\
                             str(node.CHstatus) + ".\n"
            node.incrementConChildren()
        else:
            if not node.alive:
                self.actionMsg = "Node " + str(self.ID) + " failed to connect; target node " + str(node.ID) +\
                                 " is dead.\n"
            elif node.CHstatus == 0:
                self.actionMsg = "Node " + str(self.ID) + " failed to connect; target node " + str(node.ID) +\
                                 " is not a CH.\n"

    def updateEnergy(self, energyCons):
        '''
        Method subtracts energy consumed from a node after the node has sent data and checks if there's enough energy
        Updates the energy consumed by the node as well
        Does also set self.alive (Boolean) which determines if node is still alive
        :param energyCons: Amount of data that was consumed
        '''
        self.energy -= energyCons
        self.nrjCons += energyCons
        self.SoC = self.energy/self.maxEnergy  # State of charge has to be updated after every energy use

        if self.energy < 0:
            self.alive = False
        else:
            self.alive = True

    def correctEnergy(self):
        '''
        Function updates the energy parameters if the energy becomes "negative"
        '''
        self.nrjCons += self.energy
        self.energy = 0
        self.SoC = self.energy / self.maxEnergy  # State of charge has to be updated after every energy use

    def sendMsg(self, sink):
        '''
        The node "sends message" to a target node. The function subtracts
        energy from this node corresponding to the amount of data packets
        sent. It also subtracts energy from the receiving node based on
        the same premises.

        This is done by manipulating the input nodes-list.

        :param nodes: List of the Nodes in the WSN
        :param sink: Sink to send msg to
        '''

        outcome = False   # outcome = whether the node has sent a message
        if self.CHparent:  # If the node has a CH/sink, ie. NOT a cluster head, node sends data to CH/sink
            if self.CHstatus == 0:
                    # Makes sure that the node is not a CH (e.g. not directly controlled) wont send more than one packet
                    self.PA = 1
                    
            k = self.PA * self.pSize  # k = the amount of bits that are sent
            # Calculate the energy that will be spent by transmitting signal
            ETx = sP.Eelec * k + sP.Eamp * k * self.getDistance(self.CHparent)**2
            ERx = (sP.Eelec + sP.EDA)*k  # Calculate the energy that will be spent by receiving signal
            #EC = (Eelec + EDA) * self.pSize * self.conChildren + ETx
            #if(self.ID == 9):
            #    print('PROBE PRINT: Real EC for node ' + str(EC))
            if((self.CHparent.alive) & (isinstance(self.CHparent, Node))):  # If data is sent to CH (not sink)
                self.updateEnergy(ETx)  # Updates energy for sending packet
                self.CHparent.updateEnergy(ERx)  # Update energy for receiving packets
                #print('ENERGY EXPENDED BY PARENT NODE: ' + str(ERx))

                # Following if statements checks if nodes have run out of energy due to sending or receiving data
                if self.energy >= 0 and self.CHparent.energy >= 0:
                    # If no power failure was had, data has been transmitted and received
                    self.actionMsg = "Node " + str(self.ID) + " of type " + str(self.CHstatus) +\
                                     " successfully sent to target node " + str(self.CHparent.ID) + " of type " +\
                                     str(self.CHparent.CHstatus) + '.'
                    self.PS += k + self.tempDataRec               # Update packages sent
                    self.CHparent.dataRec += k          # Update packets received for CH
                    self.CHparent.tempDataRec += k      # Update temporary packets received for CH which are then sent on to the sink as well
                    outcome = True

                if self.energy < 0:
                    self.actionMsg = "Node " + str(self.ID) +\
                                     " failed to transmit; ran out of energy while sending to node " +\
                                     str(self.CHparent.ID) + ".\n"
                    # Corrects the energy consumed by taking away the "negative" energy that isn't consumed for real
                    self.correctEnergy()

                if self.CHparent.energy < 0:
                    self.actionMsg = "Failed to transmit: node " + str(self.CHparent.ID) +\
                                     " ran out of energy while receiving from node " +\
                                     str(self.ID) + ".\n" + str(self.CHparent.ID) + str(self.ID)
                    self.CHparent.correctEnergy()
            else:
                if not self.CHparent.alive:
                    self.actionMsg = "Node " + str(self.ID) + " failed to transmit; target node " +\
                                     str(self.CHparent.ID) + " is dead.\n"
                elif self.CHparent.CHstatus == 0:
                    self.actionMsg = "Node " + str(self.ID) + " failed to transmit; target node " +\
                                     str(self.CHparent.ID) + " is not a CH. \n"

            if self.CHparent.ID == sink.ID:  # If data is sent from CH to sink
                if self.CHstatus == 0:
                    # Makes sure that a node that is not a CH (e.g. not directly controlled)
                    # won't send more than one packet
                    self.PA = 1

                # Energy is subtracted before data is transmitted since a power failure should
                # result in a faulty transmission
                self.updateEnergy(ETx)
                sink.updateEnergy(ERx)
        
                if self.energy >= 0 and sink.energy >= 0:
                    # If no power failure was had, data has been transmitted and received
                    self.actionMsg = "Node " + str(self.ID) + " successfully sent to sink " + str(sink.ID) + "!\n"
                    self.PS += k + self.tempDataRec
                    
                    sink.dataRec += self.tempDataRec + k
                    outcome = True

                if self.energy < 0:
                    self.actionMsg = "Node " + str(self.ID) +\
                                     " failed to transmit; ran out of energy while sending to sink " +\
                                     str(sink.ID) + "."
                    # Corrects the energy consumed by taking away the "negative" energy that isn't consumed for real
                    self.correctEnergy()

                if sink.energy < 0:
                    self.actionMsg = "Sink " + str(sink.ID) +\
                                     " failed to receive; ran out of energy while receiving from node " +\
                                     str(self.ID) + ".\n"
                    sink.correctEnergy()
        else:
            self.actionMsg = "Failed to transmit: Not connected to a receiver. \n"

        return outcome

    def setPR(self, desiredPR):
        '''
         Sets the amount of packets sent during coming transmissions.
         The number of desired packet rate is supposed to be a whole
         number so that only whole packages are sent.

         THOUGHT - maybe this ought to be rounded instead for more
         dynamic control signal options? For example if the controller deems
         that the packet rate should be 1.9, maybe it shouldnt stay on 1
         but rather jump up to 2

        :param desiredPR: The desired packet rate
        '''
        if(desiredPR>=1):
            if desiredPR == round(desiredPR):
                self.PA = desiredPR
            else:  # In case the desired PR is not an int, the PR is rounded to closest int. THIS MIGHT NEED TO BE CHANGED!!
                self.PA = round(desiredPR)
                print('Desired packet rate was not a whole number. The PR was rounded to closest int \n')

    def generateNRJ(self):
        '''
        Function that makes the node generate energy based on a value
        stated in params. The nrjGenFac is simply a factor multiplied with
        the max amount of energy that can be stored in the node.

        So if we for example have a max energy amount of 2J and a factor of
        0.1, we can at most harvest 0.2J each time this function is called.
        This value is multiplied with a random value between {0:1}
        to make it more "natural".
        '''

        maxNrjGenerated = self.maxEnergy * sP.nrjGenFac
        nrj_generated = random.random() * maxNrjGenerated
        self.energy = self.energy + nrj_generated

        # Energy stored in node can't exceed the max energy stored
        if self.energy > self.maxEnergy:
            self.energy = self.maxEnergy

        self.SoC = self.energy/self.maxEnergy  # State of charge has to be updated after every energy use

    def generateCHstatus(self, f, h_s, h_r, p, rnd):
        '''
        :param f: Weight between SoC and LEACH
        :param p: CH probability
        :param rnd: Random number used to determine CH status
        '''
               
        if rnd % (1 / p) == 0:
            self.CHflag = 0

        randVal = random.random()
        t = (p / (1 - p * (rnd % (1 / p))))
        if f < 1 and not self.otherBLEACH:  # If we want to try without BLEACH, we simply set f > 1
            t = (1 - f) * sP.h_s * (p / (1 - p * (rnd % (1 / p)))) * self.SoC +\
                sP.h_r*(1 / (1 - (1 - f) * (p / (1 - p * (rnd % (1 / p)))))) * f * (p / (1 - p * (rnd % (1 / p))))
        
        # Generates the t-value if otherBLEACH is True. Uses the lookup-table tVector
        # to generate a t-value according to it's state of charge.
        if(self.otherBLEACH):   
            instance = int(round(self.SoC,2)*100)
            if instance == 100:
                instance -= 1
            rndIndex = int(round(rnd % (1 / p)))
            t = self.tVector[instance][rndIndex]
            
        # If t is bigger than the randomized value, this node becomes a CH
        if t > randVal and self.CHflag == 0:
            self.CHstatus = 1
            self.CHflag = 1
        else:
            self.CHstatus = 0
            
        return t



if __name__ == "__main__":
    n = Node(1, 5, 5, 0.5)
    t = []
    p = 0.1
    for i in range(30):
        t_temp = n.generateCHstatus(1.5, 2,2,p,i)
        t.append(t_temp)
    print(t)