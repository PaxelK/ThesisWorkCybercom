function [output] = runBLEACH(SN, params)
%%%%%%%%%%%%%%%%%%%% Network Establishment paramseters %%%%%%%%%%%%%%%%%%%%

%%% Area of Operation %%%
xm = params.xm; % Field Dimensions in meters %
ym = params.ym;
x = params.x;% added for better display results of the plot
y = params.y;% added for better display results of the plot
n = params.n;% Number of Nodes in the field %
dead_nodes = params.dead_nodes;% Number of Dead Nodes in the beggining %

% Coordinates of the Sink (location is predetermined in this simulation) %
sinkx = params.sinkx;
sinky = params.sinky;

%%% Energy Values %%%
% Initial Energy of a Node (in Joules) % 
Eo = params.Eo;% units in Joules
Eelec = params.Eelec;% Energy required to run circuity (both for transmitter and receiver), units in Joules/bit
ETx = params.ETx% units in Joules/bit
ERx = params.ERx;% units in Joules/bit
Eamp = params.Eamp;% Transmit Amplifier Types, units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
EDA = params.EDA;% Data Aggregation Energy, units in Joules/bit

k = params.k;%% Size of data package, units in bits

% Suggested percentage of cluster head %
p = params.p;% a 5 percent of the total amount of nodes used in the network is proposed to give good results
No = params.No;% Number of Clusters %
rnd = params.rnd;% Round of Operation %
operating_nodes = params.operating_nodes; % Current Number of operating Nodes %
transmissions = params.transmissions;%Amount of transmissions that have been sent/recieved%
temp_val = params.temp_val;
flag1stdead = params.flag1stdead;
%Weight distribution between the term taking SoC into account and the term making sure a cluster head
%is being chosen even when all nodes have low SoC.
f = params.f;       
%%%%%%%%%%%%%%%%%%%%%%%%%%% End of paramseters %%%%%%%%%%%%%%%%%%%%%%%%%%%%


while operating_nodes>0
        
    % Displays Current Round in command window %     
    rnd     

	% Threshold Value %
	t=(p/(1-p*(mod(rnd,1/p))));
    
    % Re-election Value %
    tleft=mod(rnd,1/p);
 
	% Reseting Previous Amount Of Cluster Heads In the Network %
	CLheads=0;
    
    % Reseting Previous Amount Of Energy Consumed In the Network on the Previous Round %
    energy=0;
 
        
        
% Cluster Heads Election %
    
        for i=1:n
            SN(i).cluster=0;    % reseting cluster in which the node belongs to
            SN(i).role=0;       % reseting node role
            SN(i).chid=0;       % reseting cluster head id
            if SN(i).rleft>0
               SN(i).rleft=SN(i).rleft-1;
            end
            
            if(f>1)             %If we want to try without BLEACH, we simply set f>1
            t=(1-f)*(p/(1-p*(mod(rnd,1/p))))*SN(i).SoC + ...
                (1/(1-(1-f)*(p/(1-p*(mod(rnd,1/p))))))*f*(p/(1-p*(mod(rnd,1/p))));
            end
            
            if (SN(i).E>0) && (SN(i).rleft==0)
                generate=rand;	
                    if generate< t 
                    SN(i).role=1;	% assigns the node role of acluster head
                    SN(i).rn=rnd;	% assigns the round that the cluster head was elected to the data table
                    SN(i).tel=SN(i).tel + 1;   % amount ofd times the node has become a cluster head
                    SN(i).rleft=1/p-tleft;    % rounds for which the node will be unable to become a CH
                    SN(i).dts=sqrt((sinkx-SN(i).x)^2 + (sinky-SN(i).y)^2); % calculates the distance between the sink and the cluster head
                    CLheads=CLheads+1;	% sum of cluster heads that have been elected this round 
                    SN(i).cluster=CLheads; % cluster of which the node got elected to be cluster head
                    CL(CLheads).x=SN(i).x; % X-axis coordinates of elected cluster head
                    CL(CLheads).y=SN(i).y; % Y-axis coordinates of elected cluster head
                    CL(CLheads).id=i; % Assigns the node ID of the newly elected cluster head to an array
                    end
        
            end
        end
        
	% Fixing the size of "CL" array %
	CL=CL(1:CLheads);
  
    
    
    
% Grouping the Nodes into Clusters & caclulating the distance between node and cluster head %
     
       for i=1:n
        if  (SN(i).role==0) && (SN(i).E>0) && (CLheads>0) % if node is normal
            for m=1:CLheads
            d(m)=sqrt((CL(m).x-SN(i).x)^2 + (CL(m).y-SN(i).y)^2);
            % we calculate the distance 'd' between the sensor node that is
            % transmitting and the cluster head that is receiving with the following equation+ 
            % d=sqrt((x2-x1)^2 + (y2-y1)^2) where x2 and y2 the coordinates of
            % the cluster head and x1 and y1 the coordinates of the transmitting node
            end
        d=d(1:CLheads); % fixing the size of "d" array
        [M,I]=min(d(:)); % finds the minimum distance of node to CH (M=min. value I=index)
        [Row, Col] = ind2sub(size(d),I); % displays the Cluster Number in which this node belongs too
        SN(i).cluster=Col; % assigns node to the cluster
        SN(i).dtch= d(Col); % assigns the distance of node to CH
        SN(i).chid=CL(Col).id; % assigns id to the CH
        end
       end
       
        
       
                           %%%%%% Steady-State Phase %%%%%%
                      
  
% Energy Dissipation for normal nodes %
    
     for i=1:n
       if ((SN(i).cond==1) && (SN(i).role==0))
           if(CLheads>0)
            if SN(i).E>0
                ETx= Eelec*k + Eamp * k * SN(i).dtch^2;
                SN(i).E=SN(i).E - ETx;
                energy=energy+ETx;
            end
            % Dissipation for cluster head during reception
            if SN(SN(i).chid).E>0 && SN(SN(i).chid).cond==1 && SN(SN(i).chid).role==1
                ERx=(Eelec+EDA)*k;
                energy=energy+ERx;
                SN(SN(i).chid).E=SN(SN(i).chid).E - ERx;
                 if SN(SN(i).chid).E<=0  % if cluster heads energy depletes with reception
                    SN(SN(i).chid).cond=0;
                    SN(SN(i).chid).rop=rnd;
                    dead_nodes=dead_nodes +1;
                    operating_nodes = operating_nodes - 1
                 end
            end        
           else         %If there are no chosen cluster heads to connect to, send to sink directly
               if SN(i).E>0
                    ETx= Eelec*k + Eamp * k *(sqrt((sinkx-SN(i).x)^2 + (sinky-SN(i).y)^2))^2;  
                    SN(i).E=SN(i).E - ETx;
                    energy=energy+ETx;
                     %fprintf(['NO CLUSTER HEADS, OpNodes: ', num2str(operating_nodes), '\n'...
                      %      , '\t' , 'CLheads = ', num2str(CLheads), '\n'])
               end
           end
        
            if SN(i).E<=0       % if nodes energy depletes with transmission
                dead_nodes=dead_nodes +1;
                operating_nodes = operating_nodes - 1
                SN(i).cond=0;
                SN(i).chid=0;
                SN(i).rop=rnd;
            end      
       end
    end
    
    
    
% Energy Dissipation for cluster head nodes %
   
   for i=1:n
     if (SN(i).cond==1)  && (SN(i).role==1)
         if SN(i).E>0
            ETx= (Eelec+EDA)*k + Eamp * k * SN(i).dts^2;
            SN(i).E=SN(i).E - ETx;
            energy=energy+ETx;
         end
         if  SN(i).E<=0     % if cluster heads energy depletes with transmission
         dead_nodes=dead_nodes +1;
         operating_nodes= operating_nodes - 1;
         SN(i).cond=0;
         SN(i).rop=rnd;
         end
     end
   end

   

  
    if operating_nodes<n && temp_val==0
        temp_val=1;
        flag1stdead=rnd
    end
    % Display Number of Cluster Heads of this round %
    %CLheads;
   
    
    if CLheads~=0
    transmissions=transmissions+1;
    end
    
 
    % Next Round %
    rnd= rnd +1;
    
    tr(transmissions)=operating_nodes;
    op(rnd)=operating_nodes;
    

    if energy>0
    nrg(transmissions)=energy;
    end
    

end


sum=0;
for i=1:flag1stdead
    sum=nrg(i) + sum;
end

temp1=sum/flag1stdead;
temp2=temp1/n;

for i=1:flag1stdead
avg_node(i)=temp2;
end

params.nrg = nrg;
params.op = op;
params.avg_node = avg_node;
params.tr = tr;

%%% Area of Operation %%%
params.xm = xm; % Field Dimensions in meters %
params.ym = ym;
params.x = x;% added for better display results of the plot
params.y = y;% added for better display results of the plot
params.n = n;% Number of Nodes in the field %
params.dead_nodes = dead_nodes;% Number of Dead Nodes in the beggining %

% Coordinates of the Sink (location is predetermined in this simulation) %
params.sinkx = sinkx;
params.sinky = sinky;

%%% Energy Values %%%
% Initial Energy of a Node (in Joules) % 
params.Eo = Eo;% units in Joules
params.Eelec = Eelec;% Energy required to run circuity (both for transmitter and receiver), units in Joules/bit
params.ETx = ETx;% units in Joules/bit
params.ERx = ERx;% units in Joules/bit
params.Eamp = Eamp;% Transmit Amplifier Types, units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
params.EDA = EDA;% Data Aggregation Energy, units in Joules/bit

params.k = k;%% Size of data package, units in bits

% Suggested percentage of cluster head %
params.p = p;% a 5 percent of the total amount of nodes used in the network is proposed to give good results
params.No = No;% Number of Clusters %
params.rnd = rnd;% Round of Operation %
params.operating_nodes = operating_nodes; % Current Number of operating Nodes %
params.transmissions = transmissions;%Amount of transmissions that have been sent/recieved%
params.temp_val = temp_val;
params.flag1stdead= flag1stdead;
%Weight distribution between the term taking SoC into account and the term making sure a cluster head
%is being chosen even when all nodes have low SoC.
params.f = f;       
%%%%%%%%%%%%%%%%%%%%%%%%%%% End of paramseters %%%%%%%%%%%%%%%%%%%%%%%%%%%%

output = params;

end

