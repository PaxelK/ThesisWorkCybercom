function [env] = setEnv(params, emode, strtNrj)
%SETENV Summary of this function goes here
%   Detailed explanation goes here
env = struct;


% Construct Sink and Node object

env.sink = Sink(params.xm, params.ym);

if (params.mode == "rand") % Random amount of energy for every node
    for i = 1:params.n;
        nrj = rand*params.maxNrj;
        env.node(i) = Node(i, rand*params.xm, rand*params.ym, nrj, params);
    end
elseif (params.mode == "dist") % Same amount of energy for every node
    nrj = strtNrj; % Amount of energy for each node [J] if 'dist' is used 
    for i = 1:params.n;
        env.node(i) = Node(i, rand*params.xm, rand*params.ym, nrj, params);
    end
else 
    fprintf("The choice of energy mode is invalid! \n")
end



end

