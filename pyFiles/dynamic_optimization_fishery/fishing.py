# specify server and application name
s = 'http://byu.apmonitor.com'
a = 'fishing'

from apm import *
apm(s,a,'clear all')
apm_load(s,a,'fishing.apm')
csv_load(s,a,'fishing.csv')

apm_option(s,a,'nlc.nodes',6)
apm_option(s,a,'nlc.solver',1)
apm_option(s,a,'nlc.imode',6)
apm_option(s,a,'nlc.mv_type',1)

apm_info(s,a,'MV','u')
apm_option(s,a,'u.status',1)
apm_option(s,a,'u.dcost',1e-5)

output = apm(s,a,'solve')
print (output)
y = apm_sol(s,a)

print ('Optimal Solution: ' + str(y['myobj'][-1]))

import matplotlib.pyplot as plt
plt.figure(1)

plt.subplot(3,1,1)
plt.plot(y['time'],y['x'],'b--',linewidth=2)
plt.legend(['x'])

plt.subplot(3,1,2)
plt.plot(y['time'],y['u'],'r.-',linewidth=2)
plt.legend(['u'])
plt.axis([0,10,0.5,1.2])

plt.subplot(3,1,3)
plt.plot(y['time'],y['myobj'],'g-',linewidth=2)
plt.legend(['myObj'])

plt.xlabel('Time')
plt.show()
