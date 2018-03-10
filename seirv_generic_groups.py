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
t_end = 52
t_start = 1
t_step = 1
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
            lamda = sum([PopIn[j]*contacts[i][j] for j in range(groups_num)]) * max(np.cos(t*6.28/52.0),10**-7)
            Eqs[i] = - beta[i]  * lamda * PopIn[i]
        if states[i] is 'e':
            lamda = sum([PopIn[j]*contacts[i-1][j] for j in range(groups_num)]) * max(np.cos(t*6.28/52.0),10**-7)
            Eqs[i] = beta[i] * lamda * PopIn[i-1] - sigma * PopIn[i] + beta[i] * (1-vac_eff) * PopIn[i+3]
        if states[i] is 'i':
            Eqs[i] = sigma * PopIn[i-1] - gamma[i] * PopIn[i]
        if states[i] is 'r':
            Eqs[i] = gamma[i] * PopIn[i-1]
        if states[i] is 'v':
            Eqs[i] = -(1-vac_eff) * beta[i] * PopIn[i]



    return Eqs

def model_4_test():
    # return 10 models with different vaccination coverage
    SIR = [spi.odeint(eq_system, PopIn, t_interval,args=([p_val]*len(model.groups),)) for p_val in np.arange(0, 1, 0.1)]
    return SIR

def model_result_dict(result):
    dictionary = dict(zip([str(g) for g in model.groups], result[-1]))
    return dict((key,value) for key, value in dictionary.iteritems() if key[-1] is 'r')

def model_result_lst(result):
    return np.array(model_result_dict(result).values())


def run_model(p):
    return spi.odeint(eq_system, PopIn, t_interval,args=(p,))

def export_to_csv(p):
    res = run_model(p)
    with open("results.csv", "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow([str(g) for g in model.groups])
        writer.writerows(res)


