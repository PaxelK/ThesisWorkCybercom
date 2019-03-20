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
        states              % Current systems states
        rnd
        nodesAlive
        EClist
        PackReclist
        meanEClist
        deadNodes
        posNodes
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
            obj.rnd = 1;
            obj.nodesAlive = [];
            obj.EClist = [];
            obj.PackReclist = [];
            obj.meanEClist = [];
            obj.deadNodes = [];
            obj.posNodes = [];
            
            tempNRJ = 0;
            for node=obj.nodes
                tempNRJ = tempNRJ + node.nrjCons;
                if(node.alive)
                    obj.nodesAlive = [obj.nodesAlive, node];
                else
                    obj.deadNodes = [obj.deadNodes, node];
                end
            end
            
            nrjMean = 0;
            if(~isempty(obj.nodesAlive))
                nrjMean = tempNRJ/length(obj.nodesAlive);
            end
            
            obj.EClist = [obj.EClist, tempNRJ];
            obj.PackReclist = [obj.PackReclist, obj.sink.dataRec];
            obj.meanEClist = [obj.meanEClist, nrjMean];
            
            for node = obj.nodesAlive
                [xnd, ynd] = node.getPos();
                obj.posNodes = [obj.posNodes; xnd, ynd];               
            end
 
        end
        
        function obj = updateEnv(obj, deltaX, deltaY, packetRates)
            %{
            METHOD updateEnv
               Input: deltaX = Sink movement in x
                      deltaY = Sink movement in y
                      packetRates = Packet rates for each CH in system
                                    (is an array of IDs with corresponding PA-values)
            
               The method moves the sink and updates the amount of packets
               that the cluster heads are to send during next transmission
               round.
            
               return: obj
            %}
            obj.sink = obj.sink.move(deltaX, deltaY);
            
            for i=1:length(packetRates)
                for j=1:length(obj.nodes)
                    if(obj.nodes(j).ID == packetRates(i,1))
                        obj.nodes(j) = obj.nodes(j).setPR(packetRates(i,2));
                    end
                end
            end
            
            
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
            obj.states = [x; y];
            for node = obj.nodes              
                [xN, yN] = node.getPos();
                obj.states = [obj.states; 
                    xN;
                    yN;
                    node.getCHstatus();
                    node.getPS();
                    node.getEC()
                    ];
            end
            states = obj.states;
        end
        
        function obj = cluster(obj)
            %{
            METHOD cluster
                    
            Iterates through all nodes and makes decide whether to be a CH
            or not with generateCHstatus().
            
            After that, it iterates through all nodes that arent CHs and
            compares it's distance to sink to all distances to all nodes
            that are CHs. It uses the index jshortest to store which
            distance was the shortest. If no distance to a CH was shorter
            than the distance to the sink, the node simply connects to the
            sink.
            %}
            for i=1:length(obj.nodes)                                                   % Check if node is alive, then generate its CHS
                if(obj.nodes(i).alive)
                    obj.nodes(i) = obj.nodes(i).generateCHstatus(obj.params.f, obj.params.p, obj.rnd);
                else
                    obj.nodes(i).CHstatus = 0;
                end
            end  
            
            for i=1:length(obj.nodes)   
               if(obj.nodes(i).getCHstatus == 0)                                        % If node is a simple node
                   minDistance = obj.nodes(i).getDistance(obj.sink);                    % Starts off with the distance to sink
                   jshortest = -1;                                                      % jshortest starts of as a "non index" number
                   for j=1:length(obj.nodes)                                            
                       if(obj.nodes(j).CHstatus == 1)                                   % Checks all cluster head nodes
                            if(minDistance > obj.nodes(i).getDistance(obj.nodes(j)))    
                                minDistance = obj.nodes(i).getDistance(obj.nodes(j));   % If distance to cluster head j was shorter than what has been measured before, make this the new minimum distance
                                jshortest = j;                                          % Store index of this node
                            end
                       end
                   end
                   if(jshortest > 0)                                                    % If a CH with in-between distance shorter than that to the sink, connect to this CH
                       obj.nodes(i) = obj.nodes(i).connect(obj.nodes(jshortest));
                   else
                       obj.nodes(i) = obj.nodes(i).connect(obj.sink);                   % Otherwise connect to the sink
                   end
               else
                   obj.nodes(i) = obj.nodes(i).connect(obj.sink);
               end
            end
        end
        
        function obj = communicate(obj)
        %{
        METHOD COMMUNICATE
        The method simply tells all nodes that are alive to send (use sendMsg()) on whichever node
        is connected to it via the parentCH-property.
            
        If the transmission fails, an "action message" generated by the failing node is printed.
        %}
            for i=1:length(obj.nodes)
                if(obj.nodes(i).alive)
                    [obj.nodes, obj.sink, outcome] = obj.nodes(i).sendMsg(obj.nodes, obj.sink);
                    if(~outcome)
                        fprintf('Node %d failed to send to node %d:\n', obj.nodes(i), obj.nodes(i).CHparent)
                        actionmsg = obj.nodes(i).getActionMsg();
                        fprintf(actionmsg + '\n');
                    end
                end
            end
        end
        
        function obj = iterateRound(obj)
        %{
        METHOD ITERATEROUND
            
        The method summarizes stats for energy consumed, packets sent, and
        node/sink position during the current round; everything that is of
        interest to plot.
            
        It then iterates the rnd-property by one step.   
        %}
            tempNRJ = 0;
            obj.nodesAlive = [];
            obj.deadNodes = [];
            
            for node=obj.nodes
                tempNRJ = tempNRJ + node.nrjCons;
                if(node.alive)
                    obj.nodesAlive = [obj.nodesAlive, node];
                else
                    obj.deadNodes = [obj.deadNodes, node];
                end
            end
            
            nrjMean = 0;
            if(~isempty(obj.nodesAlive))
                nrjMean = tempNRJ/length(obj.nodesAlive);
            end
            
            obj.EClist = [obj.EClist, tempNRJ];
            obj.PackReclist = [obj.PackReclist, obj.sink.dataRec];
            obj.meanEClist = [obj.meanEClist, nrjMean];
            
            obj.posNodes = [];
            for node = obj.nodesAlive
                [xnd, ynd] = node.getPos();
                obj.posNodes = [obj.posNodes; xnd, ynd];               
            end 
            obj.rnd = obj.rnd + 1;
        end
        
            
        function [ecSUM, ecList] = getECstats(obj)
        % Returns both the sum of all energy consumed and the list of
        % energy consumed each round.
            ecList = obj.EClist;
            ecSUM = sum(obj.EClist);
        end
        
        function [prSUM, prList] = getPRstats(obj)
        % Returns both the sum of all bits received and the list of
        % bits received each round.
            prList = obj.PackReclist;
            prSUM = sum(obj.PackReclist);
        end
        
        function meanEClist = getECmeanStats(obj)
        % Returns a list of the mean energy consumption per node for for
        % each round.
            meanEClist = obj.meanEClist;
        end
        
        function [nDead, deadList] = getDeadNodes(obj)
        % Returns the list of all dead nodes.
            deadList = obj.deadNodes;
            nDead = sum(obj.deadNodes);
        end
    end
end