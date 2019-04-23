# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:34:38 2019

@author: axkar1
"""
from scipy.optimize import minimize
import numpy as np

Eelec = 1 #50*10^(-9)
Eamp = 1 #100*10^(-12)
EDA = 1 #5*10^(-9)
Egen = 5 #1*10^(-5)
const = 0.6
nrj = 80


conChildren = 5
pSize = 20000

stepLength = 2
packet = 1
E = 1
dStart = 10
T = 10


def objective(*arg):
    print("HEJ")
    ec = arg
    pr = np.zeros(len(arg))
    print(len(arg))
    print(ec[1])
    for i in range(len(arg)):
        print(i)
        pr[i] = (ec[i] - (Eelec+EDA)*pSize*conChildren)/(pSize*(Eelec + Eamp*distChange(dStart, i)**2))   
    bits = sum(pr)
    return bits 

def distChange(sdist, steps):
    d = sdist - stepLength*steps
    return d

cons = ({'type': 'ineq', 'fun': lambda x:  x[0]},
        {'type': 'ineq', 'fun': lambda x:  x[1]},
        {'type': 'ineq', 'fun': lambda x:  x[2]},
        {'type': 'ineq', 'fun': lambda x:  x[3]},
        {'type': 'ineq', 'fun': lambda x:  x[4]},
        {'type': 'ineq', 'fun': lambda x:  x[5]},
        {'type': 'ineq', 'fun': lambda x:  20-x[0]},
        {'type': 'ineq', 'fun': lambda x:  20-x[1]},
        {'type': 'ineq', 'fun': lambda x:  20-x[2]},
        {'type': 'ineq', 'fun': lambda x:  20-x[3]},
        {'type': 'ineq', 'fun': lambda x:  20-x[4]},
        {'type': 'ineq', 'fun': lambda x:  20-x[5]}
        )

print (minimize(lambda x: objective(x[0],x[1], x[2], x[3], x[4], x[5]), [1, 1, 1, 1, 1, 1],
               method='COBYLA',
               constraints = cons,
               options={'maxiter':50000}))    







'''

const = 1.0
hourly_pay = 12.0
minimum_production = 400

def production(hours_worked, num_employees):
    productivity = const * min(1.0 - 0.01 * (hours_worked-40), 1.10)
    return num_employees * hours_worked * productivity

def cost(hours_worked_pt, num_employees_pt, hours_worked_ft, num_employees_ft):
    part_time_labor_cost = hours_worked_pt * hourly_pay * num_employees_pt
    part_time_fixed_cost = 20*num_employees_pt
    full_time_labor_cost = hours_worked_ft * num_employees_ft * hourly_pay
    full_time_fixed_cost = 100*num_employees_ft
    return  (part_time_labor_cost
             + part_time_fixed_cost
             + full_time_labor_cost
             + full_time_fixed_cost)


cons = ({'type': 'ineq', 'fun': lambda x:  production(x[0], x[1]) + production(x[2], x[3]) - minimum_production},
        {'type': 'ineq', 'fun': lambda x:  x[0]},
        {'type': 'ineq', 'fun': lambda x:  x[1]},
        {'type': 'ineq', 'fun': Lambda x:  29-x[0]},
        {'type': 'ineq', 'fun': lambda x:  x[2] - 30},
        {'type': 'ineq', 'fun': lambda x:  x[3]},
        )



print (minimize(lambda x: cost(x[0],x[1], x[2], x[3]), [0.59, 492.0, 0, 0],
               method='COBYLA',
               constraints = cons,
               options={'maxiter':5000}))



https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.NonlinearConstraint.html#scipy.optimize.NonlinearConstraint
https://www.youtube.com/watch?v=bXAkr7MPf4w 

https://stackoverflow.com/questions/43702352/maximize-optimization-using-scipy
'''

