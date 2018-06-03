import pytest
import seirv_generic_groups
from calc_averted import generate_conf
from jinja2 import Template
from load_configuration import Model
import numpy as np

@pytest.fixture
def load_model():
    with open('popmodel-seirv.yaml') as file_:
        conf_tmpl = Template(file_.read())
    model = Model(generate_conf(conf_tmpl))
    return seirv_generic_groups.run_model(model=model)

def test_sum_to_one(load_model):
    '''
    test that the size of the population doesn't change
    :param load_model: 
    '''
    for i in load_model:
            assert(sum(i)>0.999999 and sum(i)<=1.0000001)

def test_non_negative(load_model):
    '''
    test that there are no negative populations
    :param load_model: 
    '''
    for i in load_model:
        for j in i:
            assert(j>=-0.001)

@pytest.mark.parametrize("group", ['pb_coverage','p_coverage','ib_coverage'])
def test_min_group_coverage(group):
    '''
    tests that the number of recovered with the minimal coverage (0) is greater than the current number of recovered  
    :param group: group name 
    :return: 
    '''
    with open('popmodel-seirv.yaml') as file_:
        conf_tmpl = Template(file_.read())
    d ={}
    d[group] = 0
    model = Model(generate_conf(conf_tmpl))
    changed_model = Model(generate_conf(conf_tmpl, d))
    changed_d = seirv_generic_groups.run_model(model=changed_model, r_dict=True)
    d = seirv_generic_groups.run_model(model=model, r_dict=True)
    values = np.array(list(d.values()))
    changed_values = np.array(list(changed_d.values()))
    assert sum(values) > sum(changed_values)

@pytest.mark.parametrize("group", ['pb_coverage','p_coverage','ib_coverage'])
def test_max_group_coverage(group):
    '''
    tests that the number of recovered with the maximal coverage (1) is less than the current number of recovered  
    :param group: group name 
    :return: 
    '''
    with open('popmodel-seirv.yaml') as file_:
        conf_tmpl = Template(file_.read())
    d ={}
    d[group] = 1
    model = Model(generate_conf(conf_tmpl))
    changed_model = Model(generate_conf(conf_tmpl, d))
    changed_d = seirv_generic_groups.run_model(model=changed_model, r_dict=True)
    d = seirv_generic_groups.run_model(model=model, r_dict=True)
    values = np.array(list(d.values()))
    changed_values = np.array(list(changed_d.values()))
    assert sum(values) > sum(changed_values)



def test_min_vaccination_efficiency():
    '''
    tests that the number of recovered with the minimal vaccination efficiency is greater than
     the current number of recovered  
    :return: 
    '''
    with open('popmodel-seirv.yaml') as file_:
        conf_tmpl = Template(file_.read())
    d ={}
    d['vaccine_efficacy'] = 0
    model = Model(generate_conf(conf_tmpl))
    changed_model = Model(generate_conf(conf_tmpl, d))
    changed_d = seirv_generic_groups.run_model(model=changed_model, r_dict=True)
    d = seirv_generic_groups.run_model(model=model, r_dict=True)
    values = np.array(list(d.values()))
    changed_values = np.array(list(changed_d.values()))
    assert sum(values) < sum(changed_values)

def test_max_vaccination_efficiency():
    '''
    tests that the number of recovered with the maximal vaccination efficiency is less than
     the current number of recovered  
    :return: 
    '''
    with open('popmodel-seirv.yaml') as file_:
        conf_tmpl = Template(file_.read())
    d ={}
    d['vaccine_efficacy'] = 1
    model = Model(generate_conf(conf_tmpl))
    changed_model = Model(generate_conf(conf_tmpl, d))
    changed_d = seirv_generic_groups.run_model(model=changed_model, r_dict=True)
    d = seirv_generic_groups.run_model(model=model, r_dict=True)
    values = np.array(list(d.values()))
    changed_values = np.array(list(changed_d.values()))
    assert sum(values) > sum(changed_values)







