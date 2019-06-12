import csv
import random

import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *

with open('nodePlacement.csv', mode='w', newline='') as node_file:
    nodePlacement_writer = csv.writer(node_file, delimiter=',')

    xPosVec = []
    yPosVec =[]

    for i in range(numNodes): # x and y coordinates
        xPosVec.append(random.random()*xSize)
        yPosVec.append(random.random()*ySize)

    nodePlacement_writer.writerow(xPosVec)
    nodePlacement_writer.writerow(yPosVec)
