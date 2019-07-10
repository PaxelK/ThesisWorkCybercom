clc, clear all, close all

t = [];

p = 0.1;               

episode = 1/p;
rnd = 0;


for i = 1:episode
    t = [t, (p / (1 - p * mod(rnd, 1/p)))];    
    rnd = rnd+1;
end
rndVec = 0:length(t)-1;
figure(1)
    h1 = plot(rndVec, t, 'color', 'r');

    legend([h1(1)], 'LEACH')
    ylim([0 1])
    xlim([0 (episode-1)])
    xlabel('Rounds')
    ylabel('T(rnd, SoC)')





