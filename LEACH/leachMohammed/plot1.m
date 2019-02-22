% Mohammad Hossein Homaei, Homaei@wsnlab.org & Homaei@wsnlab.ir
% Ver 1. 10/2014
figure(1), hold on
plot(nodeArch.nodesLoc(:, 1), nodeArch.nodesLoc(:, 2),...
    '.', 'MarkerSize',15);
plot(netArch.Sink.x, netArch.Sink.y,'o', ...
    'MarkerSize',8, 'MarkerFaceColor', 'g');