import pytest
import seirv_generic_groups

@pytest.fixture
def load_model():
    return seirv_generic_groups.run_model()

def test_sum_to_one(load_model):
        for i in load_model:
                assert(sum(i)>0.999999 and sum(i)<=1.0000001)

def test_non_negative(load_model):
    # test that there are no negative populations
        for i in load_model:
            for j in i:
                assert(j>=-0.001)







