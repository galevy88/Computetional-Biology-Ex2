
import numpy as np
from ypstruct import structure 
import warnings
from ga_functions import *
from loss_functions import *
warnings.filterwarnings("ignore", category=RuntimeWarning)

decoded_text_file = "plain.txt"
best_solution_file = "perm.txt"

def local_search(candidate, N=1):
    alphabet = np.array(list(alpha_set))  # list of possible characters
    for _ in range(N):
        neighbor = candidate.deepcopy()
        # Pick a random index
        index = np.random.randint(len(neighbor.sequence))
        # Replace the character at the chosen index with a different random character from the alphabet
        new_char = np.random.choice(alphabet)
        neighbor.sequence[index] = new_char
        neighbor.fitness = fitness(neighbor.sequence)
        if neighbor.fitness > candidate.fitness:
            candidate = neighbor
    return candidate



def run_ga():

    # Parameters
    maxit = 150
    npop = 50
    beta = 1
    pc = 2
    nc = int(np.round(pc * npop / 2) * 2)  
    mu = 0.05

    empty_individual = structure()
    empty_individual.sequence = None
    empty_individual.fitness = None

    bestsol = empty_individual.deepcopy()
    bestsol.fitness = -np.inf

    pop = empty_individual.repeat(npop)
    for i in range(npop):
        pop[i].sequence = np.random.permutation(alpha_set.copy())
        pop[i].fitness = fitness(pop[i].sequence)
        if pop[i].fitness > bestsol.fitness:
            bestsol = pop[i].deepcopy()

    bestcost = np.empty(maxit)
    avgcost = np.empty(maxit)
    bestseq = []

    # Main Loop
    for it in range(maxit):
        costs = np.array([x.fitness for x in pop])
        avg_cost = np.mean(costs)
        if avg_cost != 0:
            costs = costs / avg_cost
        probs = np.exp(-beta * costs)
        probs /= np.sum(probs)

        avgcost[it] = avg_cost

        print(f"Generation : {it}")


        popc = []
        for _ in range(nc // 2): 
            p1 = pop[roulette_wheel_selection(probs)]
            p2 = pop[roulette_wheel_selection(probs)]

            c1, c2 = crossover(p1, p2)

            c1 = mutate(c1, mu)
            c2 = mutate(c2, mu)
            
            # Lamarckian
            c1 = local_search(c1)
            c1.fitness = fitness(c1.sequence)
            if c1.fitness > bestsol.fitness:
                bestsol = c1.deepcopy()

            # Lamarckian
            c2 = local_search(c2)
            c2.fitness = fitness(c2.sequence)
            if c2.fitness > bestsol.fitness:
                bestsol = c2.deepcopy()

            popc.append(c1)
            popc.append(c2)

            pop += popc
            pop = sorted(pop, key=lambda x: x.fitness, reverse=True) 
            pop = pop[:npop] 

            bestcost[it] = bestsol.fitness
            bestseq.append(bestsol.sequence)


    return bestsol.sequence, bestcost, avgcost

if __name__ == '__main__':
    best_solution, best_fitness_array, avg_fitness_array = run_ga()
    create_output(best_solution, decoded_text_file, best_solution_file)
    print(G.COUNTER)