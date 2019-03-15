classdef EnvironmentEngine
    %{
        EnvironmentEngine acts as an interactive environment
        where input signals controlling the sink position and
        packet rate of each cluster head node.
    %}
    properties
        sink                % Holds one sink object
        nodes               % Holds an array containing all nodes of the WSN
        params              % Parameters used for setting up the network
    end
    
    methods
        function obj = EnvironmentEngine()
            %{
            The constructor uses the function setup() to initiate and
            create all nodes and the sink, which are returned in the
            array "env".  
            %}
            [parameters, env] = setup();
            obj.params = parameters;
            obj.sink = env{1}{1};
            obj.nodes = env{2};
        end
        
        function obj = updateEnv(obj, deltaX, deltaY, packetRates)
            %{
            METHOD updateEnv
               Input: deltaX = Sink movement in x
                      deltaY = Sink movement in y
                      packetRates = Packet rates for each CH in system
                                    (is supposed to be an array of vals)
            
               The method moves the sink and updates the amount of packets
               that the cluster heads are to send during next transmission
               round.
            
               return: obj
            %}
            obj.sink = obj.sink.move(deltaX, deltaY);
            
        end
        
        function [sinkX, sinkY, sinkDataRec] = sinkStatus(obj)
            % METHOD sinkStatus
            % Returns the status of the sink in terms of position and
            % packets received.
            [sinkX, sinkY] = obj.sink.getPos();
            sinkDataRec = obj.sink.getDataRec();
        end
        
        function states = getStates(obj) 
            %{
            METHOD getStates
            Returns the current state values of the sink and each node of
            the system with the form:
            [sinkx, sinky, nodeVals1, nodeVals2,....., nodeValsN]^T          
            %}
            [x, y] = obj.sink.getPos();
            states = [x; y];
            for node = obj.nodes
                states = [states; 
                            node.xPos;
                            node.yPos;
                            node.CHstatus;
                            node.PS;
                            node.nrjCons;
                          ];
            end
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