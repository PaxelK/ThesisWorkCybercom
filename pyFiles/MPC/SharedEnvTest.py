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
from MPCnode_v3 import MPCnode
from MPCsink import MPCsink
from MPC2ndLayerTest import MPC2ndLayer
from plotEnv import *
from setParamsMPC import *
import copy
import csv


ctrlHrz = 10
ctrlRes = ctrlHrz + 1
kill = False #Variable for exiting the greater loop

x, y = EE_MPC.sink.getPos()  # Get position/coordinates of sink


totRounds_MPC = []
totRounds_leach = []

totPacks_MPC = []
totPacks_leach = []

enQuotas = []
datQuotas = []
ppJleach = []
ppJMPC = []
ch_amounts = []

temp_MPC_en = 0
temp_leach_en = 0
temp_MPC_dat = 0
temp_leach_dat = 0

temp_ppJleach = 0
temp_ppjMPC = 0

totEn = 0


"""
The greater loop. One loop represents a round. During this loop the following steps occur:
    1. The environment is plotted, shows change in network energy and packages aggrevated
    2. The network is clustered, e.g. cluster head and non-CH roles are assigned
    3. The solvers for the 2nd layer and the sink are refreshed for the new round
    4. The 2nd layer decides on an optimal sink point-to-be, which gets relayed to the sink control,
        and an optimal amount of data to be desired from each cluster head
    5. The minor loop begins:
            The loop represents each time segment of a round. 
            During this loop the following steps occur:
                a) The sink produces an array containing its planned destination
                    for each time segment. This is for the node later accessing it
                    to be able to plan for optimal transmission timings.
                b) A for-loop is run to execute control on each CHs packet rate
                c) Transmission occurs when all is set; communicate() is called
                d) The sink moves another step on its planned route.
    6. iterateRound() is called to record network stats and prepare the network for the next round.            
"""
desdatasum = 0
actualdatasum = 0
for test in range(1):
    EE_MPC = MPC2ndLayer(ctrlHrz, ctrlRes)  # Initiate environment
    EE_leach = copy.deepcopy(EE_MPC)
    
    for node in EE_MPC.nodes:
        totEn += node.energy
        #node.otherBLEACH = True
    while True:  # Run until all node dies
    #for q in range(1):
        print(f"Round = {EE_leach.rnd}")
        
        #plotEnv(EE_leach)
        
        
        if(len(EE_MPC.deadNodes) != numNodes):
            EE_MPC.cluster()
            optimalP = EE_MPC.controlEnv()
            EE_MPC.sink.setTarPoint(optimalP[0], optimalP[1])
            
            print('Expected lifetime in rounds: {0}'.format(EE_MPC.expLifetime))
            print('Data received by sink: {0}'.format(EE_MPC.sink.dataRec))
            print('Alive nodes: {0}\nDeadNodes: {1}'.format(len(EE_MPC.nodesAlive), len(EE_MPC.deadNodes)))
            print('Number of nodes alive: {0}'.format(len(EE_MPC.nodesAlive)))
            print('Number of CHs active: {0}'.format(len(EE_MPC.CHds)))
            print('Sink Position: X={0}, Y={1}'.format(EE_MPC.sink.xPos, EE_MPC.sink.yPos))
            
            for g in EE_MPC.CHds: 
                desdatasum += g.desData
                
            EE_MPC.newCycle = True
            for i in range(time_segments): #time_segments
                print('TIME SEGMENT: {0}'.format(i))
                if i==time_segments-1:
                    for n in EE_MPC.nonCHds:
                        if n.alive and type(n.CHparent) is not MPCsink:
                            outcome = n.sendMsg(EE_MPC.sink)
                            if not outcome and EE_MPC.verbose:
                                print(f"Node {n.ID} failed to send to node {n.CHparent.ID}!\n")
                                actionmsg = n.getActionMsg()
                                print(str(actionmsg) + "\n")   
                    """  
                    # This segment is for if one wants to try without PR-control
                    for c in EE_MPC.CHds:
                        if c.alive:
                            c.setPR(1)
                            outcome = c.sendMsg(EE_MPC.sink)
                            if not outcome and EE_MPC.verbose:
                                print(f"Node {c.ID} failed to send to node {c.CHparent.ID}!\n")
                                actionmsg = c.getActionMsg()
                                print(str(actionmsg) + "\n")
                    """
                # ALL NON-CHs CONNECTED TO SINK SENDS IN BEGINNING BEFORE MOVEMENT
                if i == 0:
                    for n in EE_MPC.nonCHds:
                        if n.alive and type(n.CHparent) is MPCsink:
                            outcome = n.sendMsg(EE_MPC.sink)
                            if not outcome and EE_MPC.verbose:
                                print(f"Node {n.ID} failed to send to node {n.CHparent.ID}!\n")
                                actionmsg = n.getActionMsg()
                                print(str(actionmsg) + "\n")   
                                
                                
                EE_MPC.sink.produce_MoveVector()
                EE_MPC.sink.move(EE_MPC.sink.xMove.value[1], EE_MPC.sink.yMove.value[1])

                
                
                for c in EE_MPC.CHds:
                    if i == 0:
                        c.tempDataRec = 0
                    if c.energy>0:
                        c.controlPR(EE_MPC.sink)
                        #print(c.data.value)
                        #print('\n')
                        #c.plot()
                        #print(c.data.value)
                        outcome = c.sendMsg(EE_MPC.sink)
                        if not outcome and EE_MPC.verbose:
                            print(f"Node {c.ID} failed to send to node {c.CHparent.ID}!\n")
                            actionmsg = c.getActionMsg()
                            print(str(actionmsg) + "\n")
                
                #print('xVec: {0}, yVec: {1}'.format(EE_MPC.sink.xMove.value, EE_MPC.sink.yMove.value))
            
            #EE_MPC.iterateRound()
        
        if(len(EE_leach.deadNodes) != numNodes):
            EE_leach.cluster()
            EE_leach.newCycle = True
            EE_leach.communicate()
            #EE_leach.iterateRound()
            print('Finished leach round.')
    
        """
        If the number of dead nodes reaches the total number of nodes, the network is seen as
        dead and the loop ceases.
        """
        if len(EE_MPC.deadNodes) >= numNodes and len(EE_leach.deadNodes) >= numNodes:  # Break when all nodes have died
            print('MPC BREAKPOINT AT ROUND {0}'.format(EE_MPC.rnd))
            print('LEACH BREAKPOINT AT ROUND {0}'.format(EE_leach.rnd))
            totRounds_MPC.append(EE_MPC.rnd)
            totRounds_leach.append(EE_leach.rnd)
                
            totPacks_MPC.append(EE_MPC.sink.dataRec/ps)
            totPacks_leach.append(EE_leach.sink.dataRec/ps)
            break
        
        sumen = 0
        sumen1 = 0
        
        
        
        temp_ppJleach = 0
        temp_ppjMPC = 0
        
        for e in EE_MPC.nodes:
            sumen += e.energy
        MPC_en = totEn-sumen
        MPC_enDiff = MPC_en - temp_MPC_en
        temp_MPC_en = MPC_en
        
        for e in EE_leach.nodes:
            sumen1 += e.energy
        leach_en = totEn-sumen1   
        leach_enDiff = leach_en - temp_leach_en
        temp_leach_en = leach_en
        
        en_quota = leach_en/MPC_en
        enQuotas.append(en_quota)
        print('Energy spent for LEACH: {0}\nEnergy spent by MPC: {1}\n Quota (LEACH/MPC): {2}'.format(leach_en, MPC_en, en_quota))
        print('\n')
        
        MPC_datDiff = EE_MPC.sink.dataRec - temp_MPC_dat
        temp_MPC_dat = EE_MPC.sink.dataRec
        
        leach_datDiff = EE_leach.sink.dataRec - temp_leach_dat
        temp_leach_dat = EE_leach.sink.dataRec


        dat_quota = EE_leach.sink.dataRec/EE_MPC.sink.dataRec
        datQuotas.append(dat_quota)
        print('Packets received by LEACH: {0}\nPackets received by MPC: {1}\n Quota (LEACH/MPC): {2}'.format(EE_leach.sink.dataRec/ps, EE_MPC.sink.dataRec/ps, dat_quota))
        
        """
        ppJ_leach = EE_leach.sink.dataRec/leach_en/ps
        ppJleach.append(ppJ_leach)
        ppJ_MPC = EE_MPC.sink.dataRec/MPC_en/ps
        ppJMPC.append(ppJ_MPC)
        """
        if(leach_enDiff != 0):
            ppJ_leach = (leach_datDiff/ps)/leach_enDiff
        ppJleach.append(ppJ_leach)
        if(MPC_enDiff != 0 and MPC_datDiff != 0):    
            ppJ_MPC = (MPC_datDiff/ps)/MPC_enDiff
        ppJMPC.append(ppJ_MPC)
        print('Packets per Joule for MPC: {0}\nPackets per Joule for leach: {1}'.format(ppJ_MPC, ppJ_leach))
        print('\n\n')
        
        ch_amounts.append(len(EE_MPC.CHds))
        
        
         
        
        #if(q==2):
        #    break
        
        if(len(EE_leach.deadNodes) < numNodes):
            plotEnv(EE_leach,1)
            EE_leach.iterateRound()
        if(len(EE_MPC.deadNodes) < numNodes):
            plotEnv(EE_MPC,1) 
            for g in EE_MPC.CHds: 
                actualdatasum += g.tempDataSent
            EE_MPC.iterateRound()
        
            
pltrnds = np.linspace(1,len(ppJleach), len(ppJleach))
plt.figure(1)
plt.plot(pltrnds, ppJleach, pltrnds, ppJMPC)
plt.legend(['LEACH', 'MPC'])
plt.xlabel("Round", fontsize =11)
plt.ylabel("Pack/J", fontsize =11)
avrgppJ_MPC = sum(ppJMPC)/len(ppJMPC)
avrgppJ_leach = sum(ppJleach)/len(ppJleach)

plt.figure(2)
plt.plot(pltrnds, ch_amounts)
plt.xlabel("Round", fontsize =11)
plt.ylabel("#CHs", fontsize =11)
           
avrgppJ_MPC = sum(ppJMPC)/len(ppJMPC)
avrgppJ_leach = sum(ppJleach)/len(ppJleach)


print('Average ppJ MPC: {0}'.format(avrgppJ_MPC))
print('Average ppJ LEACH: {0}'.format(avrgppJ_leach))
print('Data Received by MPC: {0}'.format(EE_MPC.sink.dataRec))
print('Data Received by LEACH: {0}'.format(EE_leach.sink.dataRec))
print('Energy consumed by MPC: {0}'.format(MPC_en))
print('Energy consumed by LEACH: {0}'.format(leach_en))
print('Minimum ppJ by LEACH: {0}, Max ppJ by LEACH: {1}'.format(min(ppJleach), max(ppJleach)))
print('Minimum ppJ by MPC: {0}, Max ppJ by MPC: {1}'.format(min(ppJMPC), max(ppJMPC)))

tempStr = 'Results_MPCVSleachHrz10_max_' + str(test) + '.txt'
with open(tempStr, 'w', newline='') as f:
    results = csv.writer(f)
        
    results.writerow(['MPC: ', totRounds_MPC])
    results.writerow(['MPC data Rec [packets]: ', totPacks_MPC])
    results.writerow(['LEACH: ', totRounds_leach])
    results.writerow(['LEACH data Rec [packets]: ', totPacks_leach])
    
    results.writerow(['---'])
    
    results.writerow(['Energy Quota [leach/MPC]: ', enQuotas])
    results.writerow(['Data Quota [leach/MPC]: ', datQuotas])
    results.writerow(['Packets per Joule for LEACH: ', ppJleach])
    results.writerow(['Packets per Joule for MPC: ', ppJMPC])
