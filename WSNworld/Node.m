classdef Node
    %NODE Summary of this class goes here
    %   Detailed explanation goes here
    
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
            %NODE Construct an instance of this class
            %   Detailed explanation goes here
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
        
        
        function obj,outcome = connect(obj, node)
            outcome = false;
            if(node.alive && obj.CHstatus == 0)
                obj.CHparent = node;
                outcome = true;
            else
                if(~node.alive)
                    fprintf('Node %d failed to connect; target node %d is dead.\n', obj.ID, node.ID);
                elseif(obj.CHstatus == 1)
                    fprintf('Node %d failed to connect; Is a CH\n', obj.ID, node.ID);
                end
            end
            
            
        end
        
        function tempSoC =  getSoC(obj)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            tempSoC = obj.SoC;
        end
    end
end

