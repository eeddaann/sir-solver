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
contact_matrix = np.array([[0.8,0.2],[0.2,0.8]])
PopIn= (Sa0,Ia0,Ra0,Sb0,Ib0,Rb0)
betaa= 0.4
betab= 0.7
gamma=1/10.
t_end = 100
t_start = 1
t_step = .02
t_interval = np.arange(t_start, t_end, t_step)

#Solving the differential equation. Solves over t for initial conditions PopIn

def eq_system(PopIn,t):
    '''Defining SIR System of Equations'''
    #Creating an array of equations
    Eqs= np.zeros((6))
    Eqs[0]= -betaa * PopIn[0]*(PopIn[1]*contact_matrix[0,0]+PopIn[4]*contact_matrix[1,1])
    Eqs[1]= betaa * PopIn[0]*(PopIn[1]*contact_matrix[0,0]+PopIn[4]*contact_matrix[1,1]) - gamma*PopIn[1]
    Eqs[2]= gamma*PopIn[1]

    Eqs[3] = -betab * PopIn[3] *(PopIn[1]*contact_matrix[0,0]+ PopIn[4]*contact_matrix[1,1])
    Eqs[4] = betab * PopIn[3] *(PopIn[1]*contact_matrix[0,0]+ PopIn[4]*contact_matrix[1,1]) - gamma * PopIn[4]
    Eqs[5] = gamma * PopIn[4]
    return Eqs

SIR = spi.odeint(eq_system, PopIn, t_interval)

#Splitting out the curves for S, I and R from each other, in case they need
#to be used seperately
Sa=(SIR[:,0])
Ia=(SIR[:,1])
Ra=(SIR[:,2])

Sb=(SIR[:,3])
Ib=(SIR[:,4])
Rb=(SIR[:,5])

def validate():
    if Sa.all()>=0 and Sa.all()<=1:
        print("s ok")
    if Ia.all()>=0 and Ia.all()<=1:
        print("i ok")
    if Ra.all()>=0 and Ra.all()<=1:
        print("r ok")

    if Sb.all()>=0 and Sb.all()<=1:
        print("s ok")
    if Ib.all()>=0 and Ib.all()<=1:
        print("i ok")
    if Rb.all()>=0 and Rb.all()<=1:
        print("r ok")

    print(Sa+Sb+Ia+Ib+Ra+Rb)

def visualize():
    plot(range(len(Sa)),Sa)
    plot(range(len(Sb)),Sb)
    plot(range(len(Ia)),Ia)
    plot(range(len(Ib)),Ib)
    plot(range(len(Ra)),Ra)
    plot(range(len(Rb)),Rb)
    plt.show()


def warpper():
    SIR = spi.odeint(eq_system, PopIn, t_interval)
    return SIR[:,1][-1],SIR[:,4][-1]

def model_4_test():
    SIR = spi.odeint(eq_system, PopIn, t_interval)
    return SIR


print(warpper())