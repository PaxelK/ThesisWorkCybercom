function [output] = setParams(fWeight, pCH, nodeAmount, maxEnergy)

params = struct;

%%%%%%%%%%%%%%%%%%%% Network Establishment Parameters %%%%%%%%%%%%%%%%%%%%
%%% Area of Operation %%%
% Field Dimensions in meters %
params.xm=100;
params.ym=100;
params.x=0; % added for better display results of the plot
params.y=0; % added for better display results of the plot
params.n=nodeAmount;% Number of Nodes in the field %
params.dead_nodes=0;% Number of Dead Nodes in the beginning %

%%% Data Packet Info %%%
params.ps = 1000;

%%% Energy Values %%%
params.maxNrj=maxEnergy;% Initial Energy of a Node (in Joules), units in Joules
params.Eelec=50*10^(-9);% Energy required to run circuity (both for transmitter and receiver), units in Joules/bit
params.ETx=50*10^(-9); % units in Joules/bit
params.ERx=50*10^(-9); % units in Joules/bit
params.Eamp=100*10^(-12);% Transmit Amplifier Types, units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
params.EDA=5*10^(-9);% Data Aggregation Energy, units in Joules/bit
params.nrjGenFac = 0.1; % Energy factor for generated energy


%Weight distribution between the term taking SoC into account and the term making sure a cluster head
%is being chosen even when all nodes have low SoC.
params.f = fWeight;
%%%%%%%%%%%%%%%%%%%%%%%%%%% End of Parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%
params.k=4000;% Size of data package, units in bits
params.p = pCH;% Suggested percentage of cluster head, a 5 percent of the total amount of nodes used in the network is proposed to give good results

params.No=params.p*params.n; % Number of Clusters %
params.rnd=0;% Round of Operation %
params.operating_nodes=params.n-params.dead_nodes;% Current Number of operating Nodes %
params.transmissions=0; %Amount of transmissions that have been sent/recieved%
params.temp_val=0;

params.flag1stdead=0;


output = params;
end

