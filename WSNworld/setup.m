function [params, env] = setup()
%SETUP Initialize all parameters
%   Detailed explanation goes here

%  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Arguments%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  f = weight between the SoC dependent term and the fully round dependent
%  term. A value above 1 switches to the regular LEACH protocol. 
%  p = the desired percentage of CHs each round
%  n = the number of nodes in the network 
%  Eo = Maximum energy for all nodes [J]
%  Emode = energy mode, 'rand' = randomised energy distribution, 'norm' = all nodes begin with max energy 
%  numNodes = Number of nodes is WSN

% Initialization
numNodes = 100;
f = 0.6; p = 0.05; n = 100; E0 = 3;% Emode = "rand";

mode = "dist";
strtNrj = 2;        % Starting energy [J]

params = setParams(f, p, n, E0);
env = setEnv(params, mode, strtNrj)
end

