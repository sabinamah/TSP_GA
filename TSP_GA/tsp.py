import random
import numpy as np
from ypstruct import structure


def create_TSP(size=5, min_distance = 1, max_distance = 100, random= True):

    if random:
        tsp = np.zeros(shape=[size, size],)
        for i in range(size):
            for j in range(i+1,size):
                r = np.random.randint(low=min_distance, high=max_distance)
                tsp[i, j] = r
                tsp[j, i] = r
    else:
        tsp = np.array( [[ 0., 35., 27., 15., 35.],
                         [35.,  0., 32., 32., 34.],
                         [27., 32.,  0., 42., 42.],
                         [15., 32., 42.,  0., 41.],
                         [35., 34., 42., 41., 0.],])

    return tsp

# tsp = create_TSP()
# print(tsp)

# solution / chromosome / individual

def calculate_distance(solution,tsp):
    # print(solution)
    # solution = [4,2,0,1,3]
    sum_distance = 0
    for i in range(len(solution)-1):

        # try:
        city1 = solution[i]
        city2 = solution[i+1]
        # print(city1,city2)
        sum_distance = sum_distance + tsp[city1, city2]
        # except:
        #     print("Error")
    # print(sum_distance)

    return sum_distance

# calculate_distance([1,2,0,4,3])

# print(createTSP())




