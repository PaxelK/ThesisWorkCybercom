% Mohammad Hossein Homaei, Homaei@wsnlab.org & Homaei@wsnlab.ir
% Ver 1. 10/2014
clc, clear all, close all

numNodes = 10; % number of nodes
p = 0.1;

netArch  = newNetwork(100, 100, 50, 175); 
nodeArch = newNodes(netArch, numNodes);
roundArch = newRound();

plot1

par = struct;

for r = 1:roundArch.numRound
    r
    clusterModel = newCluster(netArch, nodeArch, 'leach', r, p);
    clusterModel = dissEnergyCH(clusterModel, roundArch);
    clusterModel = dissEnergyNonCH(clusterModel, roundArch);
    nodeArch     = clusterModel.nodeArch; % new node architecture after select CHs
    
    par = plotResults(clusterModel, r, par);
    if nodeArch.numDead == nodeArch.numNode % Break out of simulation if all nodes are dead
        break
    end
end


