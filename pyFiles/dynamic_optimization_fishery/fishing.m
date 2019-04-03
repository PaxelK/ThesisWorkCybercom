clear all; close all; clc

s = 'http://byu.apmonitor.com';
a = 'fishing';

addpath('apm')
apm(s,a,'clear all');
apm_load(s,a,'fishing.apm');
csv_load(s,a,'fishing.csv');

apm_option(s,a,'nlc.nodes',6);
apm_option(s,a,'nlc.solver',1);
apm_option(s,a,'nlc.imode',6);
apm_option(s,a,'nlc.mv_type',1);

apm_info(s,a,'MV','u');
apm_option(s,a,'u.status',1);
apm_option(s,a,'u.dcost',1e-5);

output = apm(s,a,'solve');
disp(output)
y = apm_sol(s,a);
z = y.x;

disp(['Optimal Solution: ' num2str(z.myobj(end))])

figure(1)

subplot(3,1,1)
plot(z.time,z.x,'b--','linewidth',2)
legend('x')
axis tight

subplot(3,1,2)
plot(z.time,z.u,'r.-','linewidth',2)
legend('u')
axis([0 10 0.5 1.1])

subplot(3,1,3)
plot(z.time,z.myobj,'g-','linewidth',2)
legend('myObj')
axis tight

xlabel('Time')
