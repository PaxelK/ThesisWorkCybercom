# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:20:56 2019

@author: axkar1
"""

import csv

results = []

with open('Results_ObleachVSleach_RANDsprd_05.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        results.append(row)
    
    BLEACH = results[0][1:][0][1:-1].split(", ")
    bleach_packrec =results[1][1:][0][1:-1].split(", ")
    
    LEACH = results[2][1:][0][1:-1].split(", ")
    leach_packrec = results[3][1:][0][1:-1].split(", ")
    
    nrj = results[4][1:][0][1:-1].split(", ")
    
    
    
    #print(BLEACH)
    #print(bleach_packrec)
    #print(LEACH)
    #print(leach_packrec)
    for i in range(len(BLEACH)):
        BLEACH[i] = int(BLEACH[i])
        bleach_packrec[i] = float(bleach_packrec[i])
        
    for i in range(len(LEACH)):
        LEACH[i] = int(LEACH[i])
        leach_packrec[i] = float(leach_packrec[i])
        
    for i in range(len(nrj)):
        nrj[i] = float(nrj[i])
        nrj[i] = int(nrj[i])
        
    bleachPPJs = []
    leachPPJs = []
    for lel in range(len(nrj)):
        bleachPPJs.append(bleach_packrec[lel]/nrj[lel])
        leachPPJs.append(leach_packrec[lel]/nrj[lel])
    #print(BLEACH)   
    meanVal_BLEACH = sum(BLEACH)/len(BLEACH)
    meanVal_LEACH = sum(LEACH)/len(LEACH)
    
    meanVal_BL_PR = sum(bleach_packrec)/len(bleach_packrec)
    meanVal_LE_PR = sum(leach_packrec)/len(leach_packrec)
    
    meanVal_BL_PPJ = sum(bleachPPJs)/len(bleachPPJs)
    meanVal_LE_PPJ = sum(leachPPJs)/len(leachPPJs)
    print('Mean value for BLEACH: {0}\nMean value for LEACH: {1}'.format(meanVal_BLEACH, meanVal_LEACH))
    print('Mean value of packets sent for BLEACH: {0}\nMean value of packets sent for LEACH: {1}'.format(meanVal_BL_PR, meanVal_LE_PR))
    
    print('Mean value of PPJ for BLEACH: {0}\nMean value of PPJ for LEACH: {1}'.format(meanVal_BL_PPJ, meanVal_LE_PPJ))

    
    # for f03 - BLEACH 13241.06,   LEACH 13443.87