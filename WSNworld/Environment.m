clear all
close all
clc

%  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Arguments%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  f = weight between the SoC dependent term and the fully round dependent
%  term. A value above 1 switches to the regular LEACH protocol. 
%  p = the desired percentage of CHs each round
%  n = the number of nodes in the network 
%  Eo = Maximum energy for all nodes [J]
%  Emode = energy mode, 'rand' = randomised energy distribution, 'norm' = all nodes begin with max energy 

f = 0.6; p = 0.05; n = 100; E0 = 1; Emode = 'rand';

params = setParams(f, p, n, E0, Emode);

% Construct Sink and Node object

Sink = Sink(params.xm, params.ym);
Node = Node();


