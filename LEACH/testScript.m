clc
clear all
close all

                   %f      p
params = setParams(0.05, 0.05);     %First argument is f (weight between the SoC function and the regular LEACH), p is the desired percentage of CHs each round

%Create the network and all nodes which are then stored in the array of
%structs SN
[SN, params] = createNetwork(params);


params = runBLEACH(SN, params);

params = plotResults(params);



















