function [nodes, output] = createNetwork(params)

% Plotting the WSN %
for i=1:params.n
    
    SN(i).id=i;	% sensor's ID number
    SN(i).x=rand(1,1)*params.xm;	% X-axis coordinates of sensor node
    SN(i).y=rand(1,1)*params.ym;	% Y-axis coordinates of sensor node
    
    if(strcmp(params.mode,'norm'))
         SN(i).E=params.Eo;     % nodes energy levels (initially set to be equal to "Eo"
    elseif(strcmp(params.mode,'rand'))
         SN(i).E=params.Eo*rand;     % nodes energy levels (initially set to be equal to "Eo"
    end
    
    SN(i).E=params.Eo;     % nodes energy levels (initially set to be equal to "Eo"
    SN(i).role=0;   % node acts as normal if the value is '0', if elected as a cluster head it  gets the value '1' (initially all nodes are normal)
    SN(i).cluster=0;	% the cluster which a node belongs to
    SN(i).cond=1;	% States the current condition of the node. when the node is operational its value is =1 and when dead =0
    SN(i).rop=0;	% number of rounds node was operational
    SN(i).rleft=0;  % rounds left for node to become available for Cluster Head election
    SN(i).dtch=0;	% nodes distance from the cluster head of the cluster in which he belongs
    % THIS WILL BE UPDATED IN OUR CASE
    SN(i).dts=0;    % nodes distance from the sink 
    SN(i).tel=0;	% states how many times the node was elected as a Cluster Head
    SN(i).rn=0;     % round node got elected as cluster head
    SN(i).chid=0;   % node ID of the cluster head which the "i" normal node belongs to
    SN(i).SoC = SN(i).E/params.Eo;
    
    hold on;
    figure(1)
    plot(params.x,params.y,params.xm,params.ym,SN(i).x,SN(i).y,'ob',params.sinkx,params.sinky,'*r');
    title 'Wireless Sensor Network';
    xlabel '(m)';
    ylabel '(m)';
    
end
nodes = SN;
output = params;
end

