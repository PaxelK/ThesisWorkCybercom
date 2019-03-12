% Mohammad Hossein Homaei, Homaei@wsnlab.org & Homaei@wsnlab.ir
% Ver 1. 10/2014
function fig(data, r, n, yLabel, Title)
% plot data vs. round

    figure(2);
    subplot(1, 3, n);
    plot(1:r, data);
    xlabel('Round');
    ylabel(yLabel);
    title(Title);
end