clc, clear all, close all
Eelec = 50*10^(-9);   	% Energy required to run circuity (both for transmitter and receiver), units in Joules/bit
Eamp = 100*10^(-12);  	% Transmit Amplifier Types, units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
EDA = 5*10^(-9);      	% Data Aggregation Energy, units in Joules/bit
k = 1000;

maxDist = 100;
d = [1:maxDist];



conChildr = [1:maxDist];
nrj = zeros(maxDist);
nrj_dtr = zeros(maxDist);

b = 1000;

for i = 1:maxDist
    ERx = conChildr(i)*((Eelec + EDA)*k);
    for j = 1:maxDist
        ETx = Eelec * b + Eamp * b * d(j)^2;
        nrj(i, j) = ERx + ETx;
    end
end

conCh = 20;
dtr = 1190:190:20000;
ERx = conCh*((Eelec + EDA)*k);
for it = 1:maxDist
    for j = 1:maxDist
        ETx = dtr(j)*(Eelec + Eamp * d(it)^2);
        nrj_dtr(it, j) = ERx + ETx;
    end
end



ppJ = (b.*ones(maxDist) + k.*ones(maxDist).*conChildr')./(k.*(nrj));

ppJ_dtr = (dtr.*ones(maxDist) + k.*ones(maxDist).*conCh)./(k.*(nrj_dtr));

figure(1)
surfl(d, conChildr, nrj)
title('Energy Cost During Transmission Round')
xlabel('Distance [m]')
ylabel('Connected Children')
zlabel('Energy Cost')

figure(2)
surfl(d, conChildr,ppJ)
title('PPJ for Varying Distance and Connected Children')
xlabel('Distance [m]')
ylabel('Connected Children')
zlabel('PPJ')

figure(3)
surfl(d, dtr,nrj_dtr)
title('Energy Cost During Transmission Round for Varying Distance and Packets Transmitted')
xlabel('Distance [m]')
ylabel('Bits Transmitted')
zlabel('PPJ')

figure(4)
surfl(d, dtr,ppJ_dtr)
title('PPJ for Varying Distance and Packets Transmitted')
xlabel('Distance [m]')
ylabel('Bits Transmitted')
zlabel('PPJ')