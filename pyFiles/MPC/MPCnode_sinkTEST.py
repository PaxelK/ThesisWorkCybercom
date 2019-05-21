# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:25:41 2019

@author: axkar1
"""
from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from MPCnodeJH_2 import MPCnode
from MPCsink import MPCsink
from setParams import *


Hrz = 10
Res = Hrz + 1


sink = MPCsink(100, 100, Hrz,Res)
#sink.plot()
 
node = MPCnode(1,20,20,0.05,Hrz,Res)
node.CHstatus = 1
    
node1 = MPCnode(2,20,60,0.05,Hrz,Res)
node1.CHstatus = 1
    
sink = MPCsink(100, 100, Hrz,Res)
    
node.connect(sink)
node1.connect(sink)





#node.setDesData(100000)
node1.setDesData(5000)

#node.controlPR(-5)


for i in range(10):
    sink.setTarPoint(20,40)
    sink.produce_MoveVector()
    node1.controlPR1(sink)
    node1.sendMsg(sink)
    sink.move(sink.xMove.value[1], sink.yMove.value[1])
    node1.plot()






#sink.move(-30,-10)


