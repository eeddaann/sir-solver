import numpy as np
from sir_age_groups import warpper
from scipy.optimize import minimize
import operator


start_pos=np.array([0.5,0.1])
cons = ({'type': 'eq', 'fun': lambda x:  1 - sum(x)}) #TODO: ineq
bnds = tuple((0,1) for x in start_pos)

def get_utility(policy_vector,preferences, model = warpper): #sign for maximization
    utilities = []
    model_results = model(policy_vector)
    for i in range(len(preferences)):
        utilities.append(sigmoid(model_results[i],k=preferences[i]))
    return sum(utilities)*-1 #for maximization


def sigmoid(x,k=1,l=1,x0=0):
    return l/(1+np.e**k*(x-x0))


class DecisionMaker:
    def __init__(self,preferences,name=None):
        self.preferences = preferences
        self.solution,self.value = self.optimize()
        if name is None:
            self.name = '-'.join([str(i) for i in self.preferences])
        else:
            self.name = name

    def optimize(self):
        res = minimize(get_utility, start_pos, method='SLSQP', bounds=bnds ,constraints=cons,args=self.preferences)
        return res.x,res.fun*-1
    def __str__(self):
        return "name:"+ self.name + " preferences:"+ str(self.preferences) + " solution:"+str(self.solution) + " value:" + str(self.value)






def elections(decision_makers):
    d = {}
    for decision_maker in decision_makers:
        d[decision_maker.name] = 0
        current_solution = decision_maker.solution
        for another_decision_maker in decision_makers:
            normalized_utility = get_utility(current_solution,another_decision_maker.preferences)/another_decision_maker.value*-1
            d[decision_maker.name] += normalized_utility
    winner = max(d, key=d.get)
    
    return sorted(d.items(), key=operator.itemgetter(1))



a = DecisionMaker([1.2,3])
b = DecisionMaker([3,1.2])
print(elections([a,b]))
dm_lst = [DecisionMaker((8 - 1) * np.random.random_sample(size=2) + 1) for i in range(100)]
print(elections(dm_lst))
#policy_vector = np.array([0.333,0.244])