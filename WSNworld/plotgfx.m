function plotgfx(environmentEngine)
%PLOTRESULTS Summary of this function goes here
%   Detailed explanation goes here
 % Plotting Simulation Results "Operating Nodes per Round" %
    env = environmentEngine;
    nodePos = env.posNodes;
    [xs, ys] = env.sink.getPos();
    [ECsum, ECstats] = env.getECstats();
    [PRsum, PRstats] = env.getPRstats();
    meanEC = env.getECmeanStats();
    [ndead, deadNodes] = env.getDeadNodes();
  
 figure(1), 
 hold off 
 nodePlot = plot(nodePos(:, 1), nodePos(:, 2),'.', 'MarkerSize',15);
 hold on 
 sinkPlot = plot(xs,ys,'o', 'MarkerSize',8, 'MarkerFaceColor', 'g');
 
  


% Create figure

figure1 = figure(2);
set(gcf, 'Position',  [100, 100, 1000, 1000])
% Create sub-plot
subplot1 = subplot(1,3,3,'Parent',figure1);
box(subplot1,'on');
hold(subplot1,'all');

% Create plot
plot(1:env.rnd, ECstats,'Parent',subplot1,'LineWidth',2,'Color',[0 1 0]);

% Create x-label
xlabel('Round','FontWeight','bold','FontSize',11,'FontName','Cambria');

% Create y-label
ylabel('sum of energy','FontWeight','bold','FontSize',11,...
    'FontName','Cambria');

% Create title
title('Sum of EC vs. round','FontWeight','bold','FontSize',12,...
    'FontName','Cambria');

% Create sub-plot
subplot2 = subplot(1,3,1,'Parent',figure1);
box(subplot2,'on');
hold(subplot2,'all');

% Create plot
plot(1:env.rnd,PRstats,'Parent',subplot2,'LineWidth',2);

% Create x-label
xlabel('Round','FontWeight','bold','FontSize',11,'FontName','Cambria');

% Create y-label
ylabel('Sum of bits sent to sink','FontWeight','bold','FontSize',11,...
    'FontName','Cambria');

% Create title
title('Number of packet sent to BS vs. round','FontWeight','bold',...
    'FontSize',12,...
    'FontName','Cambria');

% Create sub-plot
subplot3 = subplot(1,3,2,'Parent',figure1);
box(subplot3,'on');
hold(subplot3,'all');

% Create plot
plot(1:env.rnd,ndead,'Parent',subplot3,'LineWidth',2,'Color',[1 0 0]);

% Create x-label
xlabel('Round','FontWeight','bold','FontSize',11,'FontName','Cambria');

% Create y-label
ylabel('# of dead nodes','FontWeight','bold','FontSize',11,...
    'FontName','Cambria');

% Create title
title('Number of dead node vs. round','FontWeight','bold','FontSize',12,...
    'FontName','Cambria');
end

