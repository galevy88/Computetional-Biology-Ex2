import numpy as np
import Globals as G
import ga_functions
import random
import string
import warnings
from loss_functions import fitness, l2_loss, l1_loss, zero_one_loss
from ypstruct import structure
warnings.filterwarnings("ignore", category=RuntimeWarning)


G.get_content()


def create_individual_dictonary():
    individual = {}
    letters = list(string.ascii_lowercase)
    random.shuffle(letters)
    for letter in string.ascii_lowercase:
        individual[letter] = letters.pop()
    return individual


def create_letter_probs(individual):
    num_letters = len(individual.dictonary)
    letter_probs = {letter: 1 / num_letters for letter in individual.dictonary}
    return letter_probs



def run():
    
    costfunc = zero_one_loss
    type = 'pair'
    npop = 100
    maxit = 1000
    beta = 1
    mu = 0.5
    update_vec = [0,1]
    pc = 2
    nc = int(np.round(pc*npop/2)*2)
    
    
    # Empty Individual Template
    empty_individual = structure()
    empty_individual.dictonary = None
    empty_individual.letter_probs = None
    empty_individual.cost = None

    # Best Solution Ever Found
    bestsol = empty_individual.deepcopy()
    bestsol.cost = np.inf
    
        # Initialize Population
    pop = empty_individual.repeat(npop)
    for i in range(npop):
        pop[i].dictonary = create_individual_dictonary()
        pop[i].letter_probs = create_letter_probs(pop[i])
        pop[i].cost = fitness(pop[i], G.ENC, costfunc, type)
        if pop[i].cost < bestsol.cost:
            bestsol = pop[i].deepcopy()

    # Best Cost of Iterations
    bestcost = np.empty(maxit)
    
     # Main Loop
    for it in range(maxit):
        costs = np.array([x.cost for x in pop])
        avg_cost = np.mean(costs)
        if avg_cost != 0:
            costs = costs/avg_cost
        probs = np.exp(-beta*costs)

        popc = []
        for _ in range(nc // 2):
            p1 = pop[ga_functions.roulette_wheel_selection(probs)]
            p2 = pop[ga_functions.roulette_wheel_selection(probs)]

            c1, c2 = ga_functions.crossover(p1, p2, update_vec)
            
            c1 = ga_functions.mutate(c1, mu)
            c2 = ga_functions.mutate(c2, mu)

            # Update fitness for c1 and c2 after mutation
            c1.cost = fitness(c1, G.ENC, costfunc, type)
            c2.cost = fitness(c2, G.ENC, costfunc, type)

            if c1.cost < bestsol.cost:
                bestsol = c1.deepcopy()

            if c2.cost < bestsol.cost:
                bestsol = c2.deepcopy()

            popc.append(c1)
            popc.append(c2)

        # Merge, Sort and Select
        pop += popc
        pop = ga_functions.remove_duplicates(pop)
        pop = sorted(pop, key=lambda x: x.cost)
        pop = pop[0:npop]
        # Store Best Cost
        bestcost[it] = bestsol.cost

        # Show Iteration Information
        ga_functions.print_top_5(bestsol, pop, it)

run()