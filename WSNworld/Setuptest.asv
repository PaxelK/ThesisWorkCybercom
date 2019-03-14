clc, clear all, close all


% Run setup function, function has no inputs
[params, env] = setup(); 


% % Test to move sink position 
% sinkpos = env{1}{1}; 
% 
% sinkpos = sinkpos.move(30, 30);


% % Testing energy generated
% FIX: SoC must be updated when node generates energy

%  node = env{2};
%  node(5)
%  node(5) = node(5).generateNRJ();
%  node(5)
%  node(5) = node(5).generateNRJ();
%  node(5)


% % Testing generating CH status


node = env{2}; 
CHamount = 0; % Amount of CH


for i=1:100; % Hard coded for the amount of nodes
    nodeCH(i) = node(i).generateCHstatus(0.6, 0.5, 0);
    if (nodeCH(i).CHstatus == 1) 
        CHamount = CHamount + 1; % Increments the CH counter 
    end
end

CHamount

% %%%%%%%%%%%% Printing to check code %%%%%%%%%%%%%%%%%%%%%%%%%
%sinkpos 

%params
%env











