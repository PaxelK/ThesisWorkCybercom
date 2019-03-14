
clc, clear all, close all

[params, env] = setup(); % Run setup function, fcn has no inputs


% Test to move sink position 
sinkpos = env.sink.move(30, 60); 


% Testing energy generated


env.node(5).generateNRJ();
env.node(5).getEnergy()
env.node(5).generateNRJ();
env.node(5).getEnergy()
env.node(5).generateNRJ();
env.node(5).getEnergy()



% Testing generating CH status


nodeCH = env.node(5).generateCHstatus(0.6, 0.05, 1);
nodeCH = env.node(5).generateCHstatus(0.6, 0.05, 1);

nodeCH;

% %%%%%%%%%%%% Printing to check code %%%%%%%%%%%%%%%%%%%%%%%%%
%sinkpos 

%params
%env