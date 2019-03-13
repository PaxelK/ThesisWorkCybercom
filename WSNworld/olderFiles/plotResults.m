function [output] = plotResults(params)
%PLOTRESULTS Summary of this function goes here
%   Detailed explanation goes here
 % Plotting Simulation Results "Operating Nodes per Round" %
    figure(2)
    plot(1:params.rnd,params.op(1:params.rnd),'-r','Linewidth',2);
    title ({'LEACH'; 'Operating Nodes per Round';})
    xlabel 'Rounds';
    ylabel 'Operational Nodes';
    hold on;
    
    % Plotting Simulation Results  %
    figure(3)
    plot(1:params.transmissions,params.tr(1:params.transmissions),'-r','Linewidth',2);
    title ({'LEACH'; 'Operational Nodes per Transmission';})
    xlabel 'Transmissions';
    ylabel 'Operational Nodes';
    hold on;
    
    % Plotting Simulation Results  %
    figure(4)
    plot(1:params.flag1stdead,params.nrg(1:params.flag1stdead),'-r','Linewidth',2);
    title ({'LEACH'; 'Energy consumed per Transmission';})
    xlabel 'Transmission';
    ylabel 'Energy ( J )';
    hold on;
    

    % Plotting Simulation Results  %
    figure(5)
    plot(1:params.flag1stdead,params.avg_node(1:params.flag1stdead),'-r','Linewidth',2);
    title ({'LEACH'; 'Average Energy consumed by a Node per Transmission';})
    xlabel 'Transmissions';
    ylabel 'Energy ( J )';
    hold on;


output = params;
end

