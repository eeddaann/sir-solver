#!/usr/bin/env python


import numpy as np
from pylab import *
import scipy.integrate as spi



#Parameter Values
Sa0 = 0.499995
Sb0 = 0.499995
Ia0 = 0.000005
Ib0 = 0.000005
Ra0 = 0.0
Rb0 = 0.0
Ida=0.0
Idb=0.0
Va=0.0
Vb=0.0
contact_matrix = np.array([[0.4,0.1],[0.1,0.4]])
PopIn= (Sa0,Ia0,Ra0,Sb0,Ib0,Rb0,Ida,Idb,Va,Vb)
betaa= 0.4
betab= 0.7
gamma=1/10.
vac_eff= 0.5
t_end = 100
t_start = 1
t_step = .02
t_interval = np.arange(t_start, t_end, t_step)
p= [0.5,0.6]
#Solving the differential equation. Solves over t for initial conditions PopIn

def eq_system(PopIn,t,p):
    '''Defining SIR System of Equations'''
    #Creating an array of equations
    Eqs= np.zeros((10))
    #sa
    Eqs[0]= -betaa * PopIn[0]*(PopIn[1]*contact_matrix[0,0]+PopIn[4]*contact_matrix[1,1]) * (1-p[0]) - p[0] * PopIn[0]
    #Ia
    Eqs[1]= betaa * PopIn[0]*(PopIn[1]*contact_matrix[0,0]+PopIn[4]*contact_matrix[1,1]) * (1-p[0]) - gamma*PopIn[1]
    #Ra
    Eqs[2]= gamma*PopIn[1] + gamma * PopIn[7]

    #Sb
    Eqs[3] = -betab * PopIn[3] *(PopIn[1]*contact_matrix[0,0]+ PopIn[4]*contact_matrix[1,1]) * (1-p[1]) - p[1] * PopIn[3]
    #Ib
    Eqs[4] = betab * PopIn[3] *(PopIn[1]*contact_matrix[0,0]+ PopIn[4]*contact_matrix[1,1]) * (1-p[1]) - gamma * PopIn[4]
    #Rb
    Eqs[5] = gamma * PopIn[4] + gamma * PopIn[9]

    #Va
    Eqs[6] = p[0] * PopIn[0] - vac_eff * betaa * PopIn[6]
    #I_da
    Eqs[7] = vac_eff * betaa * PopIn[6] - gamma * PopIn[7]

    # Va
    Eqs[8] = p[1] * PopIn[3] - vac_eff * betab * PopIn[8]
    # I_da
    Eqs[9] = vac_eff * betab * PopIn[8] - gamma * PopIn[9]

    return Eqs

SIR = spi.odeint(eq_system, PopIn, t_interval,args=(p,))

#Splitting out the curves for S, I and R from each other, in case they need
#to be used seperately
Sa=(SIR[:,0])
Ia=(SIR[:,1])
Ra=(SIR[:,2])

Sb=(SIR[:,3])
Ib=(SIR[:,4])
Rb=(SIR[:,5])


def visualize():
    plot(range(len(Sa)),Sa)
    plot(range(len(Sb)),Sb)
    plot(range(len(Ia)),Ia)
    plot(range(len(Ib)),Ib)
    plot(range(len(Ra)),Ra)
    plot(range(len(Rb)),Rb)
    plt.show()


def warpper(p):
    SIR = spi.odeint(eq_system, PopIn, t_interval,args=(p,))
    return SIR[:,1][-1]+SIR[:,7][-1],SIR[:,4][-1]+SIR[:,9][-1]

def model_4_test():
    SIR = spi.odeint(eq_system, PopIn, t_interval,args=(p,))
    return SIR


