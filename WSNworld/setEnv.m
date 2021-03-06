function [env] = setEnv(params, emode, strtNrj)
%SETENV Sets the simulation environment
%   This function initializes the simulation environment

env = {};

sinkInstance = Sink(params.xm, params.ym); % Create instance of sink

env = {sinkInstance};
nodeArray = [];

if (emode == "rand") % Random amount of energy for every node
    for i = 1:params.n;
        nrj = rand*params.maxNrj;
        tempVal = Node(i, rand*params.xm, rand*params.ym, nrj, params);
        nodeArray = [nodeArray, tempVal];

    end
elseif (emode == "dist") % Same amount of energy for every node
    nrj = strtNrj; % Amount of energy for each node [J] if 'dist' is used 
    for i = 1:params.n;
        tempVal = Node(i, rand*params.xm, rand*params.ym, nrj, params);
        nodeArray = [nodeArray, tempVal];
   end
else 
    fprintf("The choice of energy mode is invalid! \n")
end

env = {env, nodeArray};
end

