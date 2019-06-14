clc, clear all, close all

t = [];
t_bleach_desc = [];

t_bleach_high = [];     % Vector for T-values with energy at 0.8 SoC for all rounds
t_bleach_low = [];      % Vector for T-values with energy at 0.2 SoC for all rounds
t_bleach_zero = [];     % Vector for T-values with energy at 0 SoC for all rounds
t_bleach_ones = [];     % Vector for T-values with energy at 1 SoC for all rounds
p = 0.05;               

episode = 1/p;
rnd = 0;

leach_ones = ones(9);
leach_zeros = zeros(9);
SoC = 1:-p:p;
SoC_high = 0.8.*ones(9);  

SoC_low = 0.2.*ones(9);  

% Spread decides which value T_BLEACH_zero is to end at.
% It also makes T_BLEACH_one end at 2-spread. So it ends at an even space
% around 1.
spread = 0.8;      

h2 = spread;
f = 0.6;
   
% This was a formula calculated on paper
h1 = (2-2*spread)/(1-f);


K1 = (1-f)*h1
K2 = f*h2
for i = 1:episode
    t = [t, (p / (1 - p * mod(rnd, episode)))];
    
    t_bleach_desc = [t_bleach_desc, h1*(1 - f)*(p / (1 - p * mod(rnd, episode))) * SoC(i) + h2*(1 / (1 - (1 - f) * (p / (1 - p * mod(rnd, episode))))) * f * (p / (1 - p * mod(rnd, episode)))];
    %*(rnd/(1+mod(rnd, episode)))
    %(exp(1)/exp((episode-1)/mod(rnd, episode)))
    
    t_bleach_ones = [t_bleach_ones, h1*(1 - f) * (p / (1 - p * mod(rnd, episode))) * leach_ones(i) + h2*(1 / (1 - (1 - f) * (p / (1 - p * mod(rnd, episode))))) * f * (p / (1 - p * mod(rnd, episode)))];
    t_bleach_high = [t_bleach_high, h1*(1 - f) * (p / (1 - p * mod(rnd, episode))) * SoC_high(i) + h2*(1 / (1 - (1 - f) * (p / (1 - p * mod(rnd, episode))))) * f * (p / (1 - p * mod(rnd, episode)))];
    t_bleach_low = [t_bleach_low, h1*(1 - f) * (p / (1 - p * mod(rnd, episode))) * SoC_low(i) + h2*(1 / (1 - (1 - f) * (p / (1 - p * mod(rnd, episode))))) * f * (p / (1 - p * mod(rnd, episode)))];
    t_bleach_zero = [t_bleach_zero, h1*(1 - f) * (p / (1 - p * mod(rnd, episode))) * leach_zeros(i) + h2*(1 / (1 - (1 - f) * (p / (1 - p * mod(rnd, episode))))) * f * (p / (1 - p * mod(rnd, episode)))];
    
    if(rnd == 0)
        START_S_HIGH = h1*(1 - f) * (p / (1 - p * mod(rnd, episode))) * leach_ones(i);
        START_R_HIGH = h2*(1 / (1 - (1 - f) * (p / (1 - p * mod(rnd, episode))))) * f * (p / (1 - p * mod(rnd, episode)));
    
        START_S_LOW = h1*(1 - f) * (p / (1 - p * mod(rnd, episode))) * leach_zeros(i);
        START_R_LOW = h2*(1 / (1 - (1 - f) * (p / (1 - p * mod(rnd, episode))))) * f * (p / (1 - p * mod(rnd, episode)));
    
    end
    if(rnd == 1/p-1)
        END_S_HIGH = h1*(1 - f) * (p / (1 - p * mod(rnd, episode))) * leach_ones(i);
        END_R_HIGH = h2*(1 / (1 - (1 - f) * (p / (1 - p * mod(rnd, episode))))) * f * (p / (1 - p * mod(rnd, episode)));
    
        END_S_LOW = h1*(1 - f) * (p / (1 - p * mod(rnd, episode))) * leach_zeros(i);
        END_R_LOW = h2*(1 / (1 - (1 - f) * (p / (1 - p * mod(rnd, episode))))) * f * (p / (1 - p * mod(rnd, episode)));
    end
    
    
    rnd = rnd+1;
end


residMax = t_bleach_ones-t;
leastQuadMax = residMax*residMax'

residMin = t-t_bleach_zero;
leastQuadMin = residMin*residMin'

rndVec = 0:length(t)-1;


threeD = 0;


figure(1)
if threeD == 0
    h1 = plot(rndVec, t, 'color', 'r');
    hold on
    h2 = plot(rndVec, t_bleach_desc, 'color', 'b' );
    h3 = plot(rndVec, t_bleach_high, 'color', 'g');
    h4 = plot(rndVec, t_bleach_low, 'color', 'k');
    h5 = plot(rndVec, t_bleach_zero, 'color', 'y');
    h6 = plot(rndVec, t_bleach_ones, 'color', 'm');
    legend([h1(1) h2(1) h3(1) h4(1) h5(1) h6(1)], 'LEACH','BLEACH_{DESC}','BLEACH_{HIGH}','BLEACH_{LOW}', 'BLEACH_{ZERO}', 'BLEACH_{ONE}')
    ylim([0 1])
    xlim([0 (episode-1)])
    xlabel('Rounds')
    ylabel('T(rnd, SoC)')
elseif threeD == 1
    h1 = plot3(rndVec, leach_ones, t, 'color', 'r');
    hold on
    h2 = plot3(rndVec, SoC, t_bleach_desc, 'color', 'b' );
    h3 = plot3(rndVec, SoC_high, t_bleach_high, 'color', 'g');
    h4 = plot3(rndVec, SoC_low, t_bleach_low, 'color', 'k');
    xlabel('Rounds')
    ylabel('SoC')
    zlabel('T(rnd, SoC)')
    ylim([0 1])
    xlim([0 (episode-1)])
    title('Regular LEACH vs BLEACH')
    legend([h1(1) h2(1) h3(1) h4(1)], 'LEACH','BLEACH','BLEACH_{HIGH}','BLEACH_{LOW}')
else
    h1 = plot(rndVec, t, 'color', 'r');
    legend([h1(1)], 'LEACH')
    ylim([0 1])
    xlim([0 (episode-1)])
    xlabel('Rounds')
    ylabel('T(rnd)')
    
    figure(2)
    h2 = plot(rndVec, t_bleach_desc, 'color', 'b' );
    legend([h2(1)], 'BLEACH')
    ylim([0 1])
    xlim([0 (episode-1)])
    xlabel('Rounds')
    ylabel('T(rnd, SoC)')
    
    figure(3)
    h3 = plot(rndVec, t_bleach_high, 'color', 'g');
    legend([h3(1)], 'BLEACH_{HIGH}')
    ylim([0 1])
    xlim([0 (episode-1)])
    xlabel('Rounds')
    ylabel('T(rnd, SoC)')
    
    figure(4)
    h4 = plot(rndVec, t_bleach_low, 'color', 'k');
    legend([h4(1)],'BLEACH_{LOW}')
    ylim([0 1])
    xlim([0 (episode-1)])
    xlabel('Rounds')
    ylabel('T(rnd, SoC)')
end





