import pytest
import seirv_generic_groups

@pytest.fixture
def load_model():
    return seirv_generic_groups.model_4_test()

def test_sum_to_one(load_model):
    for model in load_model:
        for i in model:
                assert(sum(i)>0.999999 and sum(i)<=1.0000001)

def test_non_negative(load_model):
    # test that there are no negative populations
    for model in load_model:
        for i in model:
            for j in i:
                assert(j>=-0.001)

def test_consistency(load_model):
    # check that there is negative correlation between vaccination coverage and recovered population
    recovered_summary = [sum(seirv_generic_groups.model_result_lst(i)) for i in load_model]
    assert recovered_summary == sorted(recovered_summary,reverse=True)






