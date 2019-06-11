# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:25:41 2019

@author: axkar1
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from EnvironmentEngineMPC import EnvironmentEngineMPC
from plotEnv import *
from setParams import *
import copy
import csv
import multiprocessing
import os
import sys

    
def threadFunc_LEACH(EE, totRounds_leach, case):
    leach = EE
    while True:
        sys.stdout.flush()
        if(len(leach.deadNodes) != numNodes):
            leach.cluster()
            leach.communicate()
            leach.iterateRound()
        else:
            """
            If the number of dead nodes reaches the total number of nodes, the network is seen as
            dead and the loop ceases.
            """
            print('LEACH ROUND AT BREAKPOINT AT ROUND {0}'.format(leach.rnd))
            totRounds_leach[case] = leach.rnd
            break
def threadFunc_BLEACH(EE,totRounds_bleach, case):  
    BLEACH = EE
    while True:
        sys.stdout.flush()
        if(len(BLEACH.deadNodes) != numNodes):    
            BLEACH.cluster()
            BLEACH.communicate()
            BLEACH.iterateRound()  
        else:
            print('BLEACH ROUND AT BREAKPOINT AT ROUND {0}'.format(BLEACH.rnd))
            totRounds_bleach[case] = BLEACH.rnd
            break
        
        
if __name__ == '__main__':
    #totRounds_bleach = []
    #totRounds_leach = []

    totRounds_bleach = multiprocessing.Array('i', 100)
    totRounds_leach = multiprocessing.Array('i', 100)
    
    testRange = 100
    for i in range(testRange):
        
        print("Current test case: {0}".format(i))
        EE_leach = EnvironmentEngineMPC(10,11)
        EE_BLEACH = copy.deepcopy(EE_leach)
        EE_BLEACH.fParam = 0.3
             
        thr_bleach = multiprocessing.Process(target=threadFunc_BLEACH, args = (EE_BLEACH,totRounds_bleach, i,))
        thr_leach = multiprocessing.Process(target=threadFunc_LEACH, args = (EE_leach,totRounds_leach, i,))

        thr_bleach.start()
        thr_leach.start()

        thr_bleach.join()
        thr_leach.join()
    
    with open('Results_bleachVSleach.txt', 'w', newline='') as f:
        results = csv.writer(f)
        
        totrnd_leach = []
        totrnd_bleach = []
        for i in range(testRange):
            totrnd_leach.append(totRounds_leach[i])
            totrnd_bleach.append(totRounds_bleach[i])
            
        results.writerow(['BLEACH: ', totrnd_bleach])
        results.writerow(['LEACH: ', totrnd_leach])
        
        
        