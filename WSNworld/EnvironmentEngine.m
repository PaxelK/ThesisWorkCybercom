classdef EnvironmentEngine
    %ENVIRONMENTENGINE Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        sink
        nodes
    end
    
    methods
        function obj = EnvironmentEngine(parameters)
            %ENVIRONMENTENGINE Construct an instance of this class
            %   Detailed explanation goes here
            [theSink, theNodes] = setup(parameters);
            obj.sink = theSink;
            obj.nodes = theNodes;
        end
        
        function obj = updateEnv(obj, deltaX, deltaY, packetRates)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            obj.sink.move(deltaX, deltaY);
        end
    end
end


% [params, env] = setup();
% 
% while (params.dead_nodes ~= numNodes) 
%     % Run algorithm until all nodes are dead
%     
%     % Get CH status for each node st the beginning of each round
%     for i = 1:params.operating_nodes;
%         env.node(i) = env.node(i).generateCHstatus(f, p, params.rnd);
%     end
%     
%     % Connect non-CH to closest CH 
%     
%     % Send data to CH or mobile sink
%     
%     % Update energy of every node with consumed and generated energy
%     
%     % Update the amount of operating nodes and dead nodes 
%     
%     
%     params.rnd = params.rnd + 1; % Increment round counter 
% end 