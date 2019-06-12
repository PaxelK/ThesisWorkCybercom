# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:20:56 2019

@author: axkar1
"""

import csv

results = []

with open('Results_bleachVSleach.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        results.append(row)
    
    BLEACH = results[0][1:][0][1:-1].split(", ")
    bleach_packrec =results[1][1:][0][1:-1].split(", ")
    
    LEACH = results[2][1:][0][1:-1].split(", ")
    leach_packrec = results[3][1:][0][1:-1].split(", ")
    
    
    
    print(BLEACH)
    print(bleach_packrec)
    print(LEACH)
    print(leach_packrec)
    for i in range(len(BLEACH)):
        BLEACH[i] = int(BLEACH[i])
        bleach_packrec[i] = float(bleach_packrec[i])
        
    for i in range(len(LEACH)):
        LEACH[i] = int(LEACH[i])
        leach_packrec[i] = float(leach_packrec[i])
        
    meanVal_BLEACH = sum(BLEACH)/len(BLEACH)
    meanVal_LEACH = sum(LEACH)/len(LEACH)
    
    meanVal_BL_PR = sum(bleach_packrec)/len(bleach_packrec)
    meanVal_LE_PR = sum(leach_packrec)/len(leach_packrec)
    
    print('Mean value for BLEACH: {0}\nMean value for LEACH: {1}'.format(meanVal_BLEACH, meanVal_LEACH))
    print('Mean value of packets sent for BLEACH: {0}\nMean value of packets sent for LEACH: {1}'.format(meanVal_BL_PR, meanVal_LE_PR))

    
    # for f03 - BLEACH 13241.06,   LEACH 13443.87