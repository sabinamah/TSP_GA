from ypstruct import structure
import random
import ga
from tsp import calculate_distance
from tsp import create_TSP
from graph import myGraph

'''First 
   Create the problem here is (tsp)'''
#solution refers to name of the cities
#matrix ---> distances
def costFunction(solution,matrix):
    return calculate_distance(solution,matrix)


'''Second 
    Problem definition'''
problem = structure()
problem.varmin = 1
problem.varmax = 90
problem.starting_point = 0
problem.matrix = create_TSP(size = 15, max_distance=problem.varmax,min_distance=problem.varmin, random = True)
problem.nvar = problem.matrix.shape[0]
problem.costfunc = costFunction


myGraph = myGraph(tsp= problem.matrix)

'''Third 
    Parameters (Genetic Algorithms)'''
param = structure()
param.maxit = 50
param.npop = 20
param.beta = 0.1
param.pc = 0.5



'''Step 4 
    Create out from ga'''
out = ga.run(problem,param, myGraph)
'''Step 5 
    Result'''

