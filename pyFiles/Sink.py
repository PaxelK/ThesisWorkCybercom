import math


class Sink:
    # Sink class
    # This class is used for the sink.Contains movement of sink and data packets recieved
    def __init__(self, sizex=100, sizey=100):
        '''
        Constructor: Constructs an instance of the class Sink
        This method creates an instance of this class
        :param sizex: WSN size, default x = 100
        :param sizey: WSN size, default y = 100
        '''
        self.xPos = sizex / 2  # Initialize by placing sink in the middle of the WSN
        self.yPos = sizey / 2  # Initialize by placing sink in the middle of the WSN
        self.dataRec = 0  # Initial packets received is zero
        self.sizeX = sizex
        self.sizeY = sizey
        self.alive = True
        self.energy = math.inf
        self.maxEnergy = math.inf
        self.SoC = self.energy / self.maxEnergy
        self.nrjCons = 0
        self.ID = math.pi
        self.CHstatus = 1
        self.conChildren = 0

    def move(self, deltax, deltay):
        '''
        The method moves the sink and stores the updated position of the sink in self.pos
        If the sink "tries" to go out of bounds, it is placed at the border of the grid.
        :param deltax: sink movement in x
        :param deltay: sink movement in y
        :return: Sink object
        '''

        if self.xPos + deltax > self.sizeX:
            self.xPos = self.sizeX

        elif self.xPos + deltax < 0:
            self.xPos = 0

        else:
            self.xPos += deltax

        if self.yPos + deltay > self.sizeY:
            self.yPos = self.sizeY

        elif self.yPos + deltay < 0:
            self.yPos = 0
        else:
            self.yPos += deltay


        '''
        if (self.xPos + deltax <= self.sizeX and self.xPos + deltax >= 0) and\
            (self.yPos + deltay <= self.sizeY and self.yPos + deltay >= 0):
            self.xPos = self.xPos + deltax
            self.yPos = self.yPos + deltay
        '''


    def getDataRec(self):
        '''
        Gets amount of data packets received
        :return: Total amount of bits received by the sink
        '''
        return self.dataRec

    def getPos(self):
        '''
        Funtion returns the x and y pos of sink
        :return: Position of sink
        '''
        xPos = self.xPos
        yPos = self.yPos
        return xPos, yPos

    def updateSoC(self):
        '''
        This method updates the state of charge of the mobile sink
        :return: None
        '''

        self.SoC = self.energy/self.maxEnergy

    def updateEnergy(self, energyCons):
        '''
        Method subtracts energy consumed from a node after the node has sent data and checks if there's enough energy
        Updates the energy consumed by the node as well
        Does also set self.alive (Boolean) which determines if node is still alive
        :param energyCons: Amount of data that was consumed
        '''
        self.energy -= energyCons
        self.nrjCons += energyCons
        self.SoC = self.energy / self.maxEnergy  # State of charge has to be updated after every energy use

        if self.energy < 0:
            self.alive = False
        else:
            self.alive = True

    def correctEnergy(self):
        '''
        Function updates the energy parameters if the energy becomes "negative"
        '''
        #self.nrjCons += self.energy
        self.energy = 0
        self.SoC = self.energy / self.maxEnergy  # State of charge has to be updated after every energy use


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