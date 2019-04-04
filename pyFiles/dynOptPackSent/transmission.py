# specify server and application name
s = 'http://byu.apmonitor.com'
a = 'transmission'

from apm import *
apm(s,a,'clear all')
apm_load(s,a,'transmission.apm')
csv_load(s,a,'transmission.csv')

apm_option(s,a,'nlc.nodes',6)
apm_option(s,a,'nlc.solver',1)
apm_option(s,a,'nlc.imode',6)
apm_option(s,a,'nlc.mv_type',1)

apm_info(s,a,'MV','pr')
apm_option(s,a,'pr.status',1)
apm_option(s,a,'pr.dcost',1e-5)

output = apm(s,a,'solve')
print (output)
y = apm_sol(s,a)

print ('Optimal Solution: ' + str(y['myobj'][-1]))

import matplotlib.pyplot as plt
plt.figure(1)

plt.subplot(3,1,1)
plt.plot(y['time'],y['nrj'],'b--',linewidth=2)
plt.legend(['nrj'])

plt.subplot(3,1,2)
plt.plot(y['time'],y['pr'],'r.-',linewidth=2)
plt.legend(['pr'])
plt.axis([0,10,0.5,1.2])

plt.subplot(3,1,3)
plt.plot(y['time'],y['myobj'],'g-',linewidth=2)
plt.legend(['myObj'])

plt.xlabel('Time')
plt.show()
