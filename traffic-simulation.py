
from numpy.random import choice
from numpy import array, mean, std,arange
import matplotlib.pyplot as plt

population_distribution = [0.11,0.33,0.41,0.15]
driver_distribution = [0,0.0196,0.6979,0.2825]
roads = array([14.9,9.8,3.4,12.9,26.2,6.5,17,25.6,30.7,1.9])*500 # direction
elements = ['0-4', '5-19', '20-49', '50+']
iterations = [0]*10

def sample_car():
    driver_histogram[choice(elements, p=driver_distribution)] += 1
    passenger_histogram[choice(elements, p=population_distribution)] += 1
    passenger_histogram[choice(elements, p=population_distribution)] += 1

for iteration in range(len(iterations)):
    driver_histogram = dict(zip(elements, [0] * 4))
    passenger_histogram = dict(zip(elements, [0] * 4))
    for road in roads:
        for i in range(int(road)):
            sample_car()
    iterations[iteration]=(driver_histogram,passenger_histogram)

def aggregate():
    labels = list(iterations[0][0].keys())
    driver_matrix = array([array(list(iteration[0].values())) for iteration in iterations])
    passenger_matrix = array([array(list(iteration[1].values())) for iteration in iterations])
    driver_means = mean(driver_matrix,axis=0)
    passenger_means = mean(passenger_matrix,axis=0)
    driver_std = std(driver_matrix,axis=0)
    passenger_std = std(passenger_matrix,axis=0)
    print(str(labels))
    print("driver_means:"+str(driver_means))
    print("driver_std:" + str(driver_std))
    print("passenger_means:" + str(passenger_means))
    print("passenger_std:" + str(passenger_std))
    return (driver_means,driver_std,passenger_means,passenger_std,labels)

def plot():
    aggregation = aggregate()
    ind = arange(4)  # the x locations for the groups
    width = 0.35
#    p1 = plt.bar(ind, aggregation[0], width, color='#d62728', yerr=aggregation[1])
#    p2 = plt.bar(ind, aggregation[2], width, color='#2644d6', yerr=aggregation[3])
    p1 = plt.bar(ind, aggregation[0], width, yerr=aggregation[1], color='#d62728')
    p2 = plt.bar(ind, aggregation[2], width, yerr=aggregation[3], bottom=aggregation[0])

    plt.ylabel('number *')
    plt.title('* by age group')
    plt.xticks(ind, aggregation[4])
    plt.yticks(arange(0, 120000, 10000))
    plt.legend((p1[0], p2[0]), ('driver', 'passenger'))

    plt.show()


#print(passenger_histogram)
#print("total: " + str(sum(passenger_histogram.values())))
plot()
# output:
# {'0-4': 16157, '20-49': 113401, '5-19': 50604, '50+': 43188}
# total: 223350
