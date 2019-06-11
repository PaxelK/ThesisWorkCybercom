# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:20:56 2019

@author: axkar1
"""

import csv

results = []

with open('Results_bleachVSleach_f03.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        results.append(row)
    
    BLEACH = results[0][1:]
    LEACH = results[1][1:]
    
    for i in range(len(BLEACH)):
        BLEACH[i] = int(BLEACH[i][1:-1])
    
    for i in range(len(LEACH)):
        LEACH[i] = int(LEACH[i][1:-1])

    meanVal_BLEACH = sum(BLEACH)/len(BLEACH)
    meanVal_LEACH = sum(LEACH)/len(LEACH)
    
    print('Mean value for BLEACH: {0}\nMean value for LEACH: {1}'.format(meanVal_BLEACH, meanVal_LEACH))
    
    
    