import pytest
import seirv_generic_groups
from calc_averted import generate_conf
from jinja2 import Template
from load_configuration import Model

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







