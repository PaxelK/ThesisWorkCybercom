classdef Node
    %{
    NODE Summary: class that represents a simple sensor node in a WSN
    
    The node is supposed to work together with a large amount of other 
    nodes as well as a mobile sink. It stores information about it's 
    position and the data and energy aggregated while functional (having
    energy > 0).
    %}
    
    properties
        params      % "real world" parameters
        ID          % Node's ID, expressed as a number
        xPos        % Node's position in x and y
        yPos
        pSize       % Preset packet size of each message
        PA          % Packet amount = amount of packets sent each transmission round
        energy      % Current amount of energy [J] residing in node
        maxEnergy   % Max amount of energy [J] that can be stored in node
        SoC         % State of Charge = energy/maxEnergy
        CHparent    % Reference to current cluster head
        CHstatus    % Cluster head status. 1 if cluster head, 0 if not
        alive       % Boolean value indicating whether node has energy > 0 or not 
        dtr         % Distance to eventual receiver
        dataRec     % Total Data received
        PS          % Packets sent
        nrjCons     % Total Energy consumed
    end
    
    methods
        
        function obj = Node(id, x, y, nrj, parameters)
        %{
        Constructor: takes in arguments for id, position, size of packages
        that get sent during transmission, starting energy level of node,
        maximum amount of energy that can be stored by the node
        (which also lead to the current state of charge of the node)
        
        Initial amount of packets sent during each transmission is set to
        1, cluster head status is set to 0 = NOT CLUSTER HEAD.
        If node starts of with energy it is seen as alive.
        %}
            obj.params = parameters;
            obj.ID = id;
            obj.xPos = x;
            obj.yPos = y;
            obj.pSize = parameters.ps;
            obj.PA = 1;
            obj.energy = nrj;
            obj.maxEnergy = parameters.maxNrj;
            obj.SoC = obj.energy/obj.maxEnergy;
            obj.CHstatus = 0;
            obj.CHparent = [];
            obj.dataRec = 0;
            obj.PS = 0;
            obj.nrjCons = 0;
            
            
            if(obj.energy > 0)
                obj.alive = true;
            else
                obj.alive = false;
            end
            
        end
        
        function packRec = getDataRec(obj)
           packRec = obj.dataRec; 
        end
        
        function ps = getPS(obj)
           ps = obj.PS;
        end
        
        function eneCons = getEC(obj)
           eneCons = obj.nrjCons; 
        end
        
        function [x, y] = getPos(obj)
           x = obj.xPos;
           y = obj.yPos;
        end
        
        function CHS = getCHstatus(obj)
           CHS = obj.CHstatus; 
        end
        
        function obj = clearConnection(obj)
        % Sets the CHparent reference to null
            obj.CHparent = [];
        end
        
        function distance = getDistance(obj, node)
        % Returns the distance between this node and an arbitrary node.
            distance = sqrt((obj.xPos-node.xPos)^2 + (obj.yPos-node.yPos)^2);
        end
        
        function obj = updateSoC(obj)
           obj.SoC = obj.energy/obj.maxEnergy;
        end
        
        function ener = getEnergy(obj)
            ener = obj.energy;
        end
        
        function obj = connect(obj, node)               
        %{
        Connection here adds another node object as a CH reference to
        this object and is stored in CHparent. If the connection fails
        due to the target node being dead, or not being a CH, or if this 
        node is already a CH, an error message is printed out.
        %}    
            if(node.alive)
                obj.CHparent = node;
                fprintf('Node %d, of type %d, connected successfully to target node %d.\n', obj.ID, obj.CHstatus, node.ID);
            else
               if(~node.alive)
                    fprintf('Node %d failed to connect; target node %d is dead.\n', obj.ID, node.ID);
               elseif(node.CHstatus == 0)
                    fprintf('Node %d failed to connect; target node %d is not a CH.\n', obj.ID, node.ID);
               end 
            end             
        end
        
        
        
        function [obj, outcome] = sendMsg(obj)
            outcome = false;
            
            if(~isempty(obj.CHparent))
                if(obj.CHparent.alive)
                    if(obj.CHstatus == 0)
                        obj.PA = 1;             % Makes sure that a node that is not a CH (e.g. not directly controlled) wont send more than one packet
                    end
                    %{
                    The node "sends message" to a target node. The function subtracts
                    energy from this node corresponding to the amount of data packets
                    sent. It also subtracts energy from the receiving node based on
                    the same premises.
                    %}
                    tempP = obj.params;     % Takes the system parameters and converts them to a simpler format
                    k = obj.PA*obj.pSize;   % k = the amount of bits that are sent 

                    ETx = tempP.Eelec*k + tempP.Eamp * k * obj.getDistance(obj.CHparent)^2;   % Calculates the energy that will be spent by transmitting signal
                    ERx=(tempP.Eelec+tempP.EDA)*k;                      % Calculates the energy that will be spent by receiving signal

                    obj.energy = obj.energy - ETx;                      % Energy is subtracted before data is transmitted since a power failure should result in a faulty transmission
                    obj.updateSoC();                                    % State of charge has to be updated after every energy use...
                    obj.CHparent.energy = obj.CHparent.energy - ERx;
                    obj.CHparent.updateSoC();
                    obj.nrjCons = obj.nrjCons + ETx;                    % Energy cost is also added to the nodes total energy consumed
                    obj.CHparent.nrjCons = obj.CHparent.nrjCons + ERx;

                    if(obj.energy >= 0 && obj.CHparent.energy >= 0)             % If no power failure was had, data has been transmitted and received
                        fprintf('Node %d succeded to send to node %d!\n', obj.ID, obj.CHparent.ID);
                        obj.PS = obj.PS + k;
                        obj.CHparent.dataRec = obj.CHparent.dataRec + k;    
                        outcome = true;
                    end
                    if(obj.energy < 0)
                        fprintf('Failed to transmit: node %d ran out of energy while sending to node %d.\n', obj.ID, obj.CHparent.ID);
                        obj.nrjCons = obj.nrjCons + obj.energy;         % Corrects the energy consumed by taking away the "negative" energy that isnt consumed for real
                        obj.energy = 0;
                        obj.updateSoC();
                        obj.alive = false;
                    end
                    if(obj.CHparent.energy < 0)
                        fprintf('Failed to transmit: node %d ran out of energy while receiving from node %d.\n', obj.CHparent.ID, obj.ID);
                        obj.CHparent.nrjCons = obj.CHparent.nrjCons + obj.CHparent.energy;
                        obj.CHparent.energy = 0;
                        obj.CHparent.updateSoC();
                        obj.CHparent.alive = false;
                    end
                else
                    if(~obj.CHparent.alive)
                        fprintf('Node %d failed to transmit; target node %d is dead.\n', obj.ID, obj.CHparent.ID);
                    elseif(node.CHstatus == 0)
                        fprintf('Node %d failed to transmit; target node %d is not a CH.\n', obj.ID, obj.CHparent.ID);
                    end 
                end
                
            else
                fprintf('Failed to transmit: Not connected to a receiver.')  
            end    
        end
        
        function obj = setPR(obj, desiredPR)
        %{ 
         Sets the amount of packets sent during coming transmissions.
         The number of desired packet rate is supposed to be a whole
         number so that only whole packages are sent.
       
         THOUGHT - maybe this ought to be rounded instead for more
         dynamic control signal options? For example if the controller deems
         that the packet rate should be 1.9, maybe it shouldnt stay on 1
         but rather jump up to 2
        %}
           if(desiredPR == floor(desiredPR))
               obj.PA = desiredPR;
           else
               fprintf('Desired packet rate was not a whole number.')
           end
            
        end
        
        function obj = generateNRJ(obj)
        %{ 
        Function that makes the node generate energy based on a value
        stated in params. The nrjGenFac is simply a factor multiplied with
        the max amount of energy that can be stored in the node.
        
        So if we for example have a max energy amount of 2J and a factor of
        0.1, we can at most harvest 0.2J each time this function is called.
        This value is multiplied with a random value between {0:1}
        to make it more "natural".
        %}
            maxNrjGenerated = obj.maxEnergy*obj.params.nrjGenFac;
            nrj_generated = rand(1)*maxNrjGenerated;
            obj.energy = obj.energy + nrj_generated;
           
            %Energy stored in node can't exceed the max energy stored
            if (obj.energy > obj.maxEnergy)
               obj.energy = obj.maxEnergy; 
            end
            
            obj = obj.updateSoC();
            
        end
        
        function obj = generateCHstatus(obj, f, p, rnd)
            randVal = rand(1);
            t=(p/(1-p*(mod(rnd,1/p))));          
            if(f<1)             %If we want to try without BLEACH, we simply set f>1
                t=(1-f)*(p/(1-p*(mod(rnd,1/p))))*obj.SoC + ...
                    (1/(1-(1-f)*(p/(1-p*(mod(rnd,1/p))))))*f*(p/(1-p*(mod(rnd,1/p))));
            end
            %If t is bigger than the randomized value, this node becomes a
            %CH
            if(t>randVal)
                obj.CHstatus = 1;
            else
                obj.CHstatus = 0;
            end
            %fprintf('t = %d, randVal = %d, which results in CHS = %d \n', t, randVal, obj.CHstatus);
        end
    end
end

