clc
clear all
close all


params = setParams(0.2, 0.05);

%Create the network and all nodes which are then stored in the array of
%structs SN
[SN, params] = createNetwork(params);

params = runBLEACH(SN, params);

params = plotResults(params);




















