clc, clear all, close all

t = [];

p = 0.05;               

episode = 1/p;
rnd = 0;

leach_ones = ones(1,9);
leach_zeros = zeros(1,9);
SoC = 1:-p:p;
SoC_high = 0.8.*ones(1,9);  

SoC_low = 0.2.*ones(1,9);  

% Spread decides which value T_BLEACH_zero is to end at.
% It also makes T_BLEACH_one end at 2-spread. So it ends at an even space
% around 1.
spread = 0.3;      
steplen = 0.01;
for i = 1:episode
    t = [t, (p / (1 - p * mod(rnd, episode)))];
    rnd = rnd+1;
end

maxVec = t.*(1+spread);
minVec = t.*(1-spread);

rndVec = 0:length(t)-1;

vVector = []; 
for i = spread:-steplen:-spread
vVector = [vVector; t.*(1+i)];
end

hVec = zeros(1, length(spread:-0.1:-spread));

clrs = ['b','g','r','y'];

figure(1)
hold on
for i = 1:length(spread:-steplen:-spread)
    hVec(i) = plot(rndVec, vVector(i, :), 'color', clrs(mod(i,length(clrs))+1));
end

residMax = maxVec-t;
leastQuadMax = residMax*residMax'

residMin = t-minVec;
leastQuadMin = residMin*residMin'

rndVec = 0:length(t)-1;