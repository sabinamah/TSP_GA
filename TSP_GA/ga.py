import numpy as np
from ypstruct import structure
import matplotlib.pyplot as plt

def run(problem, params, myGraph):
    # problem information

    costfunc = problem.costfunc
    nvar = problem.nvar
    starting_point = problem.starting_point
    varmax = problem.varmax
    varmin = problem.varmin
    matrix = problem.matrix

    ## parameters
    maxit = params.maxit
    npop = params.npop
    beta = params.beta
    pc = params.pc   #----> PC is the number of probability of the children
    nc = int(np.round(pc*npop/2)*2)


    '''Create Intial population'''
    # empty individual template
    empty_individual = structure()
    empty_individual.position = None
    empty_individual.cost = None


    '''Create my graph'''

    fig1 = plt.figure(figsize=(6, 4),)
    ax1 = fig1.add_subplot(1, 1, 1)
    ax1.set_xlabel(f"Iteration")
    ax1.set_ylabel(f"Cost")



    '''best solution'''
    bestsol = empty_individual.deepcopy()
    # we have to find worst function by using infinity
    bestsol.cost = np.inf



    # Initialize Population
    pop = empty_individual.repeat(npop)
    for i in range(npop):

        '''concatenate uses for combine '''
        pop[i].position = np.concatenate((np.array([0]),np.random.choice(list(range(1, nvar )), size = nvar- 1, replace = False )))
        pop[i].cost = costfunc(pop[i].position, problem.matrix)
        if pop[i].cost < bestsol.cost:
            bestsol = pop[i].deepcopy()

    '''Best cost of interation'''
    bestcost = np.empty(maxit)

    # main loop
    for it in range(maxit):

        costs = [x.cost for x in pop]
        averg_cost = np.mean(costs)
        if averg_cost != 0:
            costs = costs/averg_cost
        probs = np.exp(-beta *costs)



        popc = []
        # why we divided nc into 2 because we have same children
        for _ in range(nc//2):

            '''perform ruolette wheel selection'''
            p1 = pop[routate_wheel_selection(probs)]
            p2 = pop[routate_wheel_selection(probs)]


            '''perform crossover'''
            c1, c2 = crossover(p1, p2)

            '''perform mutation'''
            c1 = mutate(c1)
            c2 = mutate(c2)


            '''Evalulate first offspring'''
            c1.cost = costfunc(c1.position, matrix)
            if c1.cost < bestsol.cost:
                bestsol = c1

            '''Evalulate second offspring'''
            c2.cost = costfunc(c2.position,matrix)
            if c2.cost < bestsol.cost:
                bestsol = c2


            '''add offspring to population'''
            popc.append(c1)
            popc.append(c2)

        '''Merge popc and pop'''
        pop += popc
        pop = sorted(pop, key=lambda x: x.cost)
        pop = pop[0:npop]

        '''Store the Best cost'''
        bestcost[it] = bestsol.cost

        '''Show the best cost'''
        print("iteration {}: Best cost = {}".format(it,bestcost[it]))



        '''Create graph'''

        line1, = ax1.plot(bestcost[:it], c='k')
        ax1.set_title(f"Best Cost: {bestsol.cost}")
        # line1.set_ydata(bestcost[:it])
        fig1.canvas.draw()

        # plt.figure('x')
        # ax.plot(bestcost[:it],c='k')
        # fig.canvas.draw()

        myGraph.plot_solution(bestsol.position, bestsol.cost)

        plt.pause(0.1)



    # output
    out = structure()
    out.pop = pop
    out.bestsol = bestsol
    out.bestcost = bestcost
    return out

def crossover(p1,p2):
    c1 = p1.deepcopy()
    c2 = p1.deepcopy()
    '''create single point'''
    cp = np.random.randint(low = 1,high=len(p1.position))

    c1.position = np.concatenate((p1.position[:cp],p2.position[cp:]))
    c2.position = np.concatenate((p2.position[:cp],p1.position[cp:]))

    #u = unique
    # c = cp
    #Unique function indicates that each element should show once
    u,c = np.unique(c1.position,return_counts=True)
    # dup1 ==> So dup1 contains the elements that appear more than once in c1.position
    dup1 = u[c>1]
    u,c = np.unique(c2.position,return_counts=True)
    dup2 =u[c>1]

# here we use loop to remove elements that repeat twice
    for i in range(len(dup1)):
        counter = 0
        for j in range(len(c1.position)):
            if c1.position[j]== dup1[i]:
                counter+=1
                if counter==2:
                    #replaced by position2
                    c1.position[j] = dup2[i]

    for i in range(len(dup2)):
        counter = 0
        for j in range(len(c2.position)):
            if c2.position[j] == dup2[i]:
                counter += 1
                if counter == 2:
                    c2.position[j] = dup1[i]

    return c1, c2
#mu = mutation rate

def mutate(x):

    y = x.deepcopy()
# 2 refers to select twice
    swap = np.random.choice(list(range(1,len(x))),2,replace=True)





    y.position[swap[0]] = x.position[swap[1]]
    y.position[swap[1]] = x.position[swap[0]]
    return y


def routate_wheel_selection(p):
    c = np.cumsum(p)
    r = np.random.rand()*sum(p)
    ind = np.argwhere(r <= c)
    return ind[0,0]