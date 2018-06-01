# coding=utf-8
from load_configuration import Model
from scipy.spatial import distance
from seirv_generic_groups import run_model
import numpy as np
from scipy.optimize import minimize, rosen, rosen_der

model = Model("popmodel-seirv.yaml")

def extract_i_infected(x):
    beta,gamma = x
    model.set_global_beta(beta) # set beta
    model.set_global_gamma(gamma)  # set gamma
    d = run_model(model=model, r_dict=True)
    return np.array([d['ij_infants_r']+d['ia_infants_r']+d['ib_infants_r'],
            d['ij_children_r']+d['ia_children_r']+d['ib_children_r'],
            d['ij_adults_r'] + d['ia_adults_r'] + d['ib_adults_r'],
            d['ij_matures_r'] + d['ia_matures_r'] + d['ib_matures_r']])/(8855000/1000.0)

def objective_func(x):
    return distance.euclidean([89.9,11.7,7.7,37.5],extract_i_infected(x))

res = minimize(objective_func, np.array([0.11721649,0.00182007]), method='Nelder-Mead', tol=0.01)
print(res.x)
print(res)

#print(extract_i_infected([ 0.11721649 , 0.00182007]))