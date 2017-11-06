import numpy as np
from scipy.optimize import minimize


def sir_model(policy_vector):
    return policy_vector

def get_utility(policy_vector,decision_maker, model = sir_model):
    utilities = []
    model_results = model(policy_vector)
    for i in range(len(decision_maker.preferences)):
        utilities.append(polynomial(model_results[i],decision_maker.preferences[i]))
    return 1- sigmoid(sum(utilities)) #1- for minimization


def sigmoid(x,k=1,l=1,x0=0):
    return l/(1+np.e**-k*(x-x0))

def polynomial(x,preference):
    return 1-x**preference

class DecisionMaker:
    def __init__(self,preferences):
        self.preferences = preferences

a = DecisionMaker([1,3,1.2])
b = DecisionMaker([3,1.1,3])
policy_vector = np.array([0.333,0.244,0.77])
model_results= sir_model(policy_vector)
utility = get_utility(model_results,a)
utility2 = get_utility(model_results,b)
res = minimize(get_utility, np.array([1,2,3]), method='Nelder-Mead', tol=1e-6,args=a)
res2 = minimize(get_utility, np.array([1,2,3]), method='Nelder-Mead', tol=1e-6,args=b)
print(res)
print(res2)
