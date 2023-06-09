import numpy as np
from ypstruct import structure 
import warnings
from ga_functions import *
from loss_functions import *
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore", category=RuntimeWarning)

decoded_text_file = "perm.txt"
best_solution_file = "plain.txt"

best_fitness_per_iteration = []

def run_ga(beta_param):

    # Parameters
    maxit = 300
    npop = 50
    beta = beta_param
    pc = 2
    nc = int(np.round(pc * npop / 2) * 2)  
    mu = 0.05
    convergence_counter = 20  # Number of iterations for convergence condition
    converged = 0  # Initialize convergence count
    last_best_fitness = None  # Initialize the last best fitness to None

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

            c1.fitness = fitness(c1.sequence)
            if c1.fitness > bestsol.fitness:
                bestsol = c1.deepcopy()

            c2.fitness = fitness(c2.sequence)
            if c2.fitness > bestsol.fitness:
                bestsol = c2.deepcopy()
            
            popc.append(c1)
            popc.append(c2)

        best_fitness_per_iteration.append(bestsol.fitness)
        pop += popc
        pop = sorted(pop, key=lambda x: x.fitness, reverse=True) 
        pop = pop[:npop] 

        bestcost[it] = bestsol.fitness
        bestseq.append(bestsol.sequence)

        # Convergence condition
        if bestsol.fitness == last_best_fitness:
            converged += 1
        else:
            converged = 0

        last_best_fitness = bestsol.fitness

        if converged >= convergence_counter:
            print(f"Convergence after {it} iterations!")
            break

    return bestsol.sequence, bestcost, avgcost

if __name__ == '__main__':
    print("Please select a mode:\nRegular - 1\nDarwinian - 2\nLamarckian - 3")
    user_input = int(input("Your selection: "))
    
    if user_input == 1:
        beta = 1
    elif user_input == 2:
        beta = 100
    elif user_input == 3:
        beta = 0
    else:
        print("Invalid selection. Defaulting to Regular mode.")
        beta = 1

    best_solution, best_fitness_array, avg_fitness_array = run_ga(beta)
    create_output(best_solution, decoded_text_file, best_solution_file)
    print(f"Total number of fitness calls: {G.COUNTER}")
    
    # Change this line to match the length of `best_fitness_per_iteration`
    iterations = range(1, len(best_fitness_per_iteration) + 1)

    plt.figure(figsize=(10, 5))
    plt.plot(iterations, best_fitness_per_iteration, label='Best Fitness per Iteration')
    plt.xlabel('Iteration')
    plt.ylabel('Best Fitness')
    plt.legend()
    plt.grid(True)
    plt.show()

