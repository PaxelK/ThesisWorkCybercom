clc
clear all
close all

%{
%Arguments:
 f = weight between the SoC function and the regular LEACH
 p = the desired percentage of CHs each round
 n = the number of nodes in the network 
 Eo = Maximum energy for all nodes
 Emode = energy mode, 'rand' = randomised energy distribution, 'norm' = all nodes begin with max energy 
 %}
                    %f    p    n   Eo  Emode
params = setParams(0.5, 0.05, 100, 1, 'rand');     

%Create the network and all nodes which are then stored in the array of
%structs SN
[SN, params] = createNetwork(params);


params = runBLEACH(SN, params);

params = plotResults(params);



















