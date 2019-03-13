classdef Node
    %{
    NODE Summary: class that represents a simple sensor node in a WSN
    
    The node is supposed to work together with a large amount of other 
    nodes as well as a mobile sink. It stores information about it's 
    position and the data and energy aggregated while functional (having
    energy > 0).
    %}
    
    properties
        ID          % Node's ID, expressed as a number
        xPos        % Node's position in x and y
        yPos
        pSize       % Preset packet size of each message
        PA          % Packet amount = amount of packets sent each transmission round
        energy      % Current amount of energy [J] residing in node
        maxEnergy   % Max amount of energy [J] that can be stored in node
        SoC         % State of Charge = energy/maxEnergy
        CHparent          % Reference to current cluster head
        CHstatus    % Cluster head status. 1 if cluster head, 0 if not
        alive
    end
    
    methods
        
        function obj = Node(id, x, y, ps, nrj, maxNrj)
        %{
        Constructor: takes in arguments for id, position, size of packages
        that get sent during transmission, starting energy level of node,
        maximum amount of energy that can be stored by the node
        (which also lead to the current state of charge of the node)
        
        Initial amount of packets sent during each transmission is set to
        1, cluster head status is set to 0 = NOT CLUSTER HEAD.
        If node starts of with energy it is seen as alive.
        %}
            obj.ID = id;
            obj.xPos = x;
            obj.yPos = y;
            obj.pSize = ps;
            obj.PA = 1;
            obj.energy = nrj;
            obj.maxEnergy = maxNrj;
            obj.SoC = obj.energy/obj.maxEnergy;
            obj.CHstatus = 0;
            
            if(obj.energy > 0)
                obj.alive = true;
            else
                obj.alive = false;
            end
            
        end
        
        
        function [obj, outcome] = connect(obj, node)
        %{
        The connect function adds another node object as a CH reference to
        this object and is stored in CHparent. If the connection fails
        due to the target node being dead, or not being a CH, or if this 
        node is already a CH, an error message is printed out. The function
        also returns true or false whether the connection was a success or
        not.
        %}
            outcome = false;
            if(node.alive && obj.CHstatus == 0)
                obj.CHparent = node;
                fprintf('Node %d succeded to connect to node %d!\n', obj.ID, node.ID);
                outcome = true;
            else
                if(~node.alive)
                    fprintf('Node %d failed to connect; target node %d is dead.\n', obj.ID, node.ID);
                elseif(obj.CHstatus == 1)
                    fprintf('Node %d failed to connect; this node is already a CH.\n', obj.ID, node.ID);
                elseif(node.CHstatus == 0)
                    fprintf('Node %d failed to connect; target node %d is not a CH.\n', obj.ID, node.ID);
                end
            end
            
            
        end

        function tempSoC =  getSoC(obj)
            %Returns the current state of charge
            tempSoC = obj.SoC;
        end
    end
end

