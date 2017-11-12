#!/usr/bin/env python


import numpy as np
from pylab import *
import scipy.integrate as spi
from load_configuration import Model

model = Model()
PopIn = [g.initial_number for g in model.groups]
PopIn = PopIn/sum(PopIn)


contacts = [g.contacts_vector for g in model.groups] #TODO: normalize
beta = [g.beta for g in model.groups]
gamma = [g.gamma for g in model.groups]
states = [g.state for g in model.groups]
vac_eff= 0.5
t_end = 100
t_start = 1
t_step = .02
t_interval = np.arange(t_start, t_end, t_step)
p = [0]*len(model.groups)
groups_num = len(model.groups)
def eq_system(PopIn,t,p):
    '''Defining SIR System of Equations'''
    #Creating an array of equations
    Eqs= np.zeros(groups_num)

    for i in range(groups_num):
        # s
        if states[i] is 's':
            Eqs[i] = - beta[i] * PopIn[i] * sum([PopIn[j]*contacts[i][j] for j in range(groups_num)]) * (1-p[i]) - p[i] * PopIn[i]
        if states[i] is 'i':
            Eqs[i] = beta[i-1] * PopIn[i-1] * sum([PopIn[j]*contacts[i-1][j] for j in range(groups_num)]) * (1-p[i-1]) - p[i-1] * PopIn[i-1] - gamma[i] * PopIn[i]
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

