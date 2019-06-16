# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:25:41 2019

@author: axkar1
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from EnvironmentEngineMPCbleach import EnvironmentEngineMPC
from plotEnv import *
#from setParams import *
import copy
import csv
import multiprocessing
import os
import sys

def threadFunc_LEACH(EE, totRounds_leach,totPackRec_leach , case):
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
            print('LEACH BREAKPOINT AT ROUND {0}'.format(leach.rnd))
            totRounds_leach[case] = leach.rnd
            totPackRec_leach[case] = leach.sink.dataRec
            break
def threadFunc_BLEACH(EE,totRounds_bleach, totPackRec_bleach, case):  
    BLEACH = EE
    while True:
        sys.stdout.flush()
        if(len(BLEACH.deadNodes) != numNodes):    
            BLEACH.cluster()
            BLEACH.communicate()
            BLEACH.iterateRound()  
        else:
            print('BLEACH BREAKPOINT AT ROUND {0}'.format(BLEACH.rnd))
            totRounds_bleach[case] = BLEACH.rnd
            totPackRec_bleach[case] = BLEACH.sink.dataRec
            break
        
        
if __name__ == '__main__':
    sprdV = np.linspace(0.5,0.1,5)
    for sprd in sprdV:
        testRange = 1
        
        totRounds_bleach = multiprocessing.Array('i', testRange)
        totRounds_leach = multiprocessing.Array('i', testRange)
        
        totPackRec_leach = multiprocessing.Array('i', testRange)
        totPackRec_bleach = multiprocessing.Array('i', testRange)
    
        
        for i in range(testRange):
            print("Current test case: {0}".format(i))
            EE_leach = EnvironmentEngineMPC(10,11)
            for a in EE_leach.nodes:
                a.otherBLEACH = True
                a.spread = sprd
            EE_BLEACH = copy.deepcopy(EE_leach)
            
            EE_BLEACH.fParam = 0.8
            EE_BLEACH.h_s_Param = 3
            EE_BLEACH.h_r_Param = 0.8
                 
            thr_bleach = multiprocessing.Process(target=threadFunc_BLEACH, args = (EE_BLEACH,totRounds_bleach, totPackRec_bleach, i,))
            thr_leach = multiprocessing.Process(target=threadFunc_LEACH, args = (EE_leach,totRounds_leach, totPackRec_leach, i,))
    
            thr_bleach.start()
            thr_leach.start()
    
            thr_bleach.join()
            thr_leach.join()
        
        fileOpenName = 'Results_ObleachVSleach_sprd_0'+str(round(sprd,1))[-1]+ '.txt'
        with open(fileOpenName, 'w', newline='') as f:
            results = csv.writer(f)
            
            totrnd_leach = []
            totrnd_bleach = []
    
            totpr_leach = []
            totpr_bleach = []
            for i in range(testRange):
                totrnd_leach.append(totRounds_leach[i])
                totrnd_bleach.append(totRounds_bleach[i])
    
                totpr_leach.append(totPackRec_leach[i]/ps)
                totpr_bleach.append(totPackRec_bleach[i]/ps)
                
            results.writerow(['BLEACH rounds: ', totrnd_bleach])
            results.writerow(['BLEACH data [packets]: ', totpr_bleach])
    
            results.writerow(['LEACH rounds: ', totrnd_leach])
            results.writerow(['LEACH data [packets]: ', totpr_leach])
  