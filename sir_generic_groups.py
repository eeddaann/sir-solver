#!/usr/bin/env python


import numpy as np
from pylab import *
import scipy.integrate as spi
from constants import groups


PopIn = [g.initial_number for g in groups]
PopIn = PopIn/sum(PopIn)

contacts = 0.5 #TODO: contacs
beta = [g.beta for g in groups]
gamma = [g.gamma for g in groups]
states = [g.state for g in groups]
vac_eff= 0.5
t_end = 100
t_start = 1
t_step = .02
t_interval = np.arange(t_start, t_end, t_step)
p = [0]*len(groups)

def eq_system(PopIn,t,p):
    '''Defining SIR System of Equations'''
    #Creating an array of equations
    Eqs= np.zeros((len(groups)))

    for i in range(len(groups)):
        # s
        if states[i] is 's':
            Eqs[i] = - beta[i] * PopIn[i] * contacts * (1-p[i]) - p[i] * PopIn[i]
        if states[i] is 'i':
            Eqs[i] = beta[i-1] * PopIn[i-1] * contacts * (1-p[i-1]) - p[i-1] * PopIn[i-1] - gamma[i] * PopIn[i]
        if states[i] is 'r':
            Eqs[i] = gamma[i] * PopIn[i-1] + gamma[i] * PopIn[i+1]
        if states[i] is 'id':
            Eqs[i] = vac_eff * beta[i] * PopIn[i+1] - gamma[i] * PopIn[i]
        if states[i] is 'v':
            Eqs[i] = p[i] * PopIn[i-4] - vac_eff * beta[i] * PopIn[i]


    return Eqs

def model_4_test():
    SIR = spi.odeint(eq_system, PopIn, t_interval,args=(p,))
    return SIR

