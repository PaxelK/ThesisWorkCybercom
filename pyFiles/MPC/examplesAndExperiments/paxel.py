from gekko import GEKKO
import numpy as np

m = GEKKO()

tf = 10   # final time
n = tf+1  # number of time points
m.time = np.linspace(0,tf,n)

# define velocity profile
vp = np.ones(n)*10
vp[3:6] = -5
v = m.Param(value=vp)

# define distance
x = m.Var(20)

# define data transmission rate
dtr = m.MV(lb=0,ub=100)
dtr.STATUS = 1

# define how much data must be transmitted
data = m.Var(500)

# energy to transmit
e = m.Intermediate(dtr*x**2*1e-5)

# equations

# track the position
m.Equation(x.dt()==v)

# as data is transmitted, remaining data stored decreases
m.Equation(data.dt() == -dtr)

# objective
m.Obj(e) # minimize energy

# soft (objective constraint)
final = m.Param(value=np.zeros(n))
final.value[-1] = 1
m.Obj(data*final) # transmit data by the end

# hard constraint
# this form may cause infeasibility if it can't achieve
#   data=0 at the end
m.fix(data,n-1,0)

# solve
m.options.IMODE = 6
m.solve()

# plot results
import matplotlib.pyplot as plt
plt.figure(1)
plt.subplot(4,1,1)
plt.plot(m.time,x.value,'r-',label='Position')
plt.legend()

plt.subplot(4,1,2)
plt.plot(m.time,v.value,'k--',label='Velocity')
plt.legend()

plt.subplot(4,1,3)
plt.plot(m.time,e.value,'b-',label='Energy')
plt.legend()

plt.subplot(4,1,4)
plt.plot(m.time,dtr.value,'r-',label='Transmission Rate')
plt.plot(m.time,data.value,'k.-',label='Data Remaining')
plt.xlabel('Time')
plt.legend()
plt.savefig('step1.png')


# update velocity
vp = np.ones(n)*10
vp[5:] = -20
v.value = vp

# solve again - states are automatically time-shifted
m.solve()

plt.figure(2)
plt.subplot(4,1,1)
plt.plot(m.time,x.value,'r-',label='Position')
plt.legend()

plt.subplot(4,1,2)
plt.plot(m.time,v.value,'k--',label='Velocity')
plt.legend()

plt.subplot(4,1,3)
plt.plot(m.time,e.value,'b-',label='Energy')
plt.legend()

plt.subplot(4,1,4)
plt.plot(m.time,dtr.value,'r-',label='Transmission Rate')
plt.plot(m.time,data.value,'k.-',label='Data Remaining')
plt.xlabel('Time')
plt.legend()
plt.savefig('step2.png')


plt.show()
