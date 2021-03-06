import numpy as np
import matplotlib.pyplot as plt
from constants import groups

def generate(vac_factors):
    eqs = []
    for group in groups:
        if group.state is 'i':
            eqs.append(np.random.poisson(4,100)*vac_factors[str(group.group)])
        else:
            np.random.poisson(4,100)

    total = sum(eqs)
    eqs = [eq/total for eq in eqs]
    # print(sum(eqs))
    # for eq in eqs:
    #     plt.plot(eq)
    #
    # plt.show()
    return eqs

print(generate({'g1':0.01,'g2':0.05}))

no_vac = generate({'g1':1,'g2':1})
vac = generate({'g1':0.5,'g2':0.5})
print(sum(sum(np.array(no_vac)-np.array(vac))))