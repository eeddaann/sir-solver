
from numpy.random import choice
from numpy import array

population_distribution = [0.11,0.33,0.41,0.15]
driver_distribution = [0,0.0196,0.6979,0.2825]
roads = array([14.9,9.8,3.4,12.9,26.2,6.5,17,25.6,30.7,1.9])*500 # direction
elements = ['0-4', '5-19', '20-49', '50+']
d = dict(zip(elements, [0]*4))
def sample_car():
    d[choice(elements, p=driver_distribution)] += 1
    d[choice(elements, p=population_distribution)] += 1
    d[choice(elements, p=population_distribution)] += 1

for road in roads:
    for i in range(int(road)):
        sample_car()

print(d)
print("total: "+str(sum(d.values())))

# output:
# {'0-4': 16157, '20-49': 113401, '5-19': 50604, '50+': 43188}
# total: 223350
