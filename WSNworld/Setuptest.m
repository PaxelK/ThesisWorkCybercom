clc, clear all, close all

% Comment: Test script for the setup.m script. The tests include to construct the 
% environment and adds the parameter in a struct. The methods in the classes are also tested.   

% Run setup function, function has no inputs
[params, env] = setup(); 

sink = env{1}{1}; % Sink is first element in env cell array
node = env{2};    % Node is second element in env cell array



% % Test to move sink position 
sink = sink.move(34, 30);
sink.xPos
sink.yPos
disp('------------------------')
sink = sink.move(-15, -25);
sink.xPos
sink.yPos
disp('------------------------')
sink = sink.move(-2, -34);
sink.xPos
sink.yPos


% % Testing energy generated

%  node = env{2};
%  node(5)
%  node(5) = node(5).generateNRJ();
%  node(5)
%  node(5) = node(5).generateNRJ();
%  node(5)
%  node(5) = node(5).generateNRJ();
%  node(5)

% % Testing generating CH status and clearing CH status


% CHamount = 0; % Amount of CH
% 
% 
% for i=1:100; % Hard coded for the amount of nodes
%     nodeCH(i) = node(i).generateCHstatus(0.6, 0.05, 0);
%     if (nodeCH(i).CHstatus == 1) 
%         CHamount = CHamount + 1; % Increments the CH counter 
%     end
% end
% 
% CHamount = 0; % Amount of CH
% 
% for i=1:100;
%     nodeCH(i) = node(i).clearConnection(); % Try to clear CH status
%     if (nodeCH(i).CHstatus == 1) 
%         CHamount = CHamount + 1; % Increments the CH counter 
%     end
% end
% 
% CHamount % Displays the amount of nodes that are CH 


% % Test getdistance methos 

% node(5).xPos
% node(5).yPos
% disp('----------------------------')
% node(6).xPos
% node(6).yPos
% disp('----------------------------')
% 
% disp('Distance from node 5 to 6')
% node(5).getDistance(node(6))
% disp('Distance from node 6 to 5')
% node(6).getDistance(node(5))





% %%%%%%%%%%%% Printing to check code %%%%%%%%%%%%%%%%%%%%%%%%%
%sinkpos 

%params
%env











