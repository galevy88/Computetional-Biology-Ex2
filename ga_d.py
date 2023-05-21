
import numpy as np
from ypstruct import structure 
import warnings
from ga_functions import *
from loss_functions import *
warnings.filterwarnings("ignore", category=RuntimeWarning)

decoded_text_file = "plain.txt"
best_solution_file = "perm.txt"

def local_search(candidate, N=10):
    for _ in range(N):
        neighbor = candidate.deepcopy()
        # Apply small random noise to the sequence as a placeholder for actual local changes.
        # Replace this with the actual local search operation for your problem.
        noise = np.random.normal(0, 0.01, size=len(neighbor.sequence))
        neighbor.sequence += noise
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
        
        # Darwinian
        c1_optimized = local_search(c1)
        c1_optimized.fitness = fitness(c1_optimized.sequence)
        if c1_optimized.fitness > bestsol.fitness:
            bestsol = c1_optimized.deepcopy()
        c1.fitness = fitness(c1.sequence)

        c2_optimized = local_search(c2)
        c2_optimized.fitness = fitness(c2_optimized.sequence)
        if c2_optimized.fitness > bestsol.fitness:
            bestsol = c2_optimized.deepcopy()
        c1.fitness = fitness(c2.sequence)

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