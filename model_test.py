import pytest
import sir_age_groups

@pytest.fixture
def load_model():
    return sir_age_groups.model_4_test()

def test_sum_to_one(load_model):
    for i in load_model:
        assert(sum(i)>0.999999 and sum(i)<=1.0000001)

def test_non_negative(load_model):
    for i in load_model:
        for j in i:
            assert(j>=-0.000001)





