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
%  numNodes = Number of nodes is WSN

[params, env] = setup();

while (params.dead_nodes ~= numNodes) 
    % Run algorithm until all nodes are dead
    
    % Get CH status for each node st the beginning of each round
    for i = 1:params.operating_nodes;
        env.node(i) = env.node(i).generateCHstatus(f, p, params.rnd);
    end
    
    % Connect non-CH to closest CH 
    
    % Send data to CH or mobile sink
    
    % Update energy of every node with consumed and generated energy
    
    % Update the amount of operating nodes and dead nodes 
    
    
    params.rnd = params.rnd + 1; % Increment round counter 
end 


% Plot the energy and data packets sent






