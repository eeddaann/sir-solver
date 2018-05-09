#!/usr/bin/env python


import numpy as np
from pylab import *
import scipy.integrate as spi
from load_configuration import Model
import csv


vac_eff= 0.2
t_end = 52
t_start = 1
t_step = 1
t_interval = np.arange(t_start, t_end, t_step)

phi = 10
sigma = 0.2


def eq_system(PopIn,t,model):
    '''Defining SIR System of Equations'''
    #Creating an array of equations
    Eqs= np.zeros(model.groups_num)

    for i in range(model.groups_num):
        if model.states[i] is 's':
            lamda = sum([PopIn[j]*model.contacts[i][j] for j in range(model.groups_num)]) * max(np.cos(t*6.28/52.0),10**-7)
            Eqs[i] = - model.beta[i]  * lamda * PopIn[i]
        if model.states[i] is 'e':
            lamda = sum([PopIn[j]*model.contacts[i-1][j] for j in range(model.groups_num)]) * max(np.cos(t*6.28/52.0),10**-7)
            Eqs[i] = model.beta[i] * lamda * PopIn[i-1] - sigma * PopIn[i] + model.beta[i] * (1-vac_eff) * PopIn[i+3]
        if model.states[i] is 'i':
            Eqs[i] = sigma * PopIn[i-1] - model.gamma[i] * PopIn[i]
        if model.states[i] is 'r':
            Eqs[i] = model.gamma[i] * PopIn[i-1]
        if model.states[i] is 'v':
            Eqs[i] = -(1-vac_eff) * model.beta[i] * PopIn[i]

    return Eqs

def run_model(path=None,model=None,export_to_csv=False,r_dict=False,r_lst=False):
    if path != None:
        model = Model(path)
    res = spi.odeint(eq_system, model.PopIn, t_interval,args=(model,))
    if export_to_csv:
        with open("results.csv", "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow([str(g) for g in model.groups])
            writer.writerows(res)
    elif r_dict:
        dictionary = dict(zip([str(g) for g in model.groups], res[-1]))
        return dict((key, value*model.total_pop) for key, value in dictionary.items() if key[-1] is 'r')
    elif r_lst:
        dictionary = dict(zip([str(g) for g in model.groups], res[-1]))
        return np.array(list(dict((key, (value*model.total_pop)) for key, value in dictionary.items() if key[-1] is 'r').values()))
        #return np.array(list(dict((key, (value * model.total_pop)) for key, value in dictionary.items() if key[-1] is 'r').values()))

    else:
        return res





