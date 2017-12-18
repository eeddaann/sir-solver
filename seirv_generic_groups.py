#!/usr/bin/env python


import numpy as np
from pylab import *
import scipy.integrate as spi
from load_configuration import Model
import csv

model = Model("popmodel-seirv.yaml")
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

phi = 10
sigma = 0.2

groups_num = len(model.groups)
def eq_system(PopIn,t,p):
    '''Defining SIR System of Equations'''
    #Creating an array of equations
    Eqs= np.zeros(groups_num)

    for i in range(groups_num):
        # s
        if states[i] is 's':
            #Eqs[i] = - beta[i] * PopIn[i] * sum([PopIn[j]*contacts[i][j] for j in range(groups_num)]) * (1-p[i]) - p[i] * PopIn[i]
            Eqs[i] = (1-p[i]) * - beta[i] * PopIn[i] * sum([PopIn[j]*contacts[i][j] for j in range(groups_num)]) * np.sin((t+phi)/52.0) - p[i] * PopIn[i+4]
        if states[i] is 'e':
            Eqs[i] = ((1-p[i]) + PopIn[i+3]*(1-vac_eff)) * beta[i] * PopIn[i-1] * sum([PopIn[j]*contacts[i-1][j] for j in range(groups_num)]) * np.sin((t+phi)/52.0) - sigma * PopIn[i]
        if states[i] is 'i':
            Eqs[i] = sigma * PopIn[i-1] - gamma[i] * PopIn[i]
        if states[i] is 'r':
            Eqs[i] = gamma[i] * PopIn[i-1]
        if states[i] is 'v':
            Eqs[i] = PopIn[i-4] * p[i] - (1-vac_eff) * beta[i] * PopIn[i-4] * sum([PopIn[j]*contacts[i-4][j] for j in range(groups_num)]) * np.sin((t+phi)/52.0)*PopIn[i]


    return Eqs

def model_4_test():
    SIR = spi.odeint(eq_system, PopIn, t_interval,args=(p,))
    return SIR

def run_model(p):
    return spi.odeint(eq_system, PopIn, t_interval,args=(p,))

def export_to_csv(p):
    res = run_model(p)
    with open("results.csv", "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow([str(g) for g in model.groups])
        writer.writerows(res)


