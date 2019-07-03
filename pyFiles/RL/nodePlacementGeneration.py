import csv
import random

import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from setParams import *

def run():
    with open('nodePlacement.csv', mode='w', newline='') as node_file:
        nodePlacement_writer = csv.writer(node_file, delimiter=',')

        xPosVec = []
        yPosVec =[]

        for i in range(numNodes): # x and y coordinates
            xPosVec.append(round(random.random()*xSize))
            yPosVec.append(round(random.random()*ySize))

        nodePlacement_writer.writerow(xPosVec)
        nodePlacement_writer.writerow(yPosVec)
