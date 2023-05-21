import numpy as np
from loss_functions import *

def create_mapping(parent, offspring, pos1, pos2):
    mapping = {}
    for i in range(pos1, pos2 + 1):
        mapping[parent.sequence[i]] = offspring[i]
    return mapping

def map_values(parent, offspring, mapping, pos1, pos2):
    for i in range(len(parent.sequence)):
        if i < pos1 or i > pos2:
            value = parent.sequence[i]
            while value in mapping:
                value = mapping[value]
            offspring[i] = value
    return offspring

def crossover(parent_a, parent_b):
    pos1 = np.random.randint(1, len(parent_a.sequence))
    pos2 = np.random.randint(pos1, len(parent_a.sequence))
    offspring_a = np.empty_like(parent_a.sequence)
    offspring_b = np.empty_like(parent_b.sequence)
    offspring_a[pos1:pos2 + 1] = parent_a.sequence[pos1:pos2 + 1]
    offspring_b[pos1:pos2 + 1] = parent_b.sequence[pos1:pos2 + 1]

    mapping_a = create_mapping(parent_a, offspring_b, pos1, pos2)
    offspring_a = map_values(parent_b, offspring_a, mapping_a, pos1, pos2)

    mapping_b = create_mapping(parent_b, offspring_a, pos1, pos2)
    offspring_b = map_values(parent_a, offspring_b, mapping_b, pos1, pos2)

    child_a, child_b = parent_a.deepcopy(), parent_b.deepcopy()
    child_a.sequence, child_b.sequence = offspring_a, offspring_b
    
    return child_a, child_b

def mutate(original, mu):
    copy = original.deepcopy()
    mutation_occurrences = np.random.rand(*original.sequence.shape) <= mu
    indices = np.argwhere(mutation_occurrences)
    if indices.size:
        for idx in indices:
            swap_idx = np.random.randint(len(original.sequence))
            copy.sequence[idx.item()], copy.sequence[swap_idx] = copy.sequence[swap_idx], copy.sequence[idx.item()]
    return copy



def roulette_wheel_selection(p):
    c = np.cumsum(p)
    r = sum(p) * np.random.rand()
    ind = np.argwhere(r <= c)
    return ind[0][0]


def create_output(solution, best_solution_file, decoded_text_file):
    
    with open(best_solution_file, 'w') as file:
        for i in range(len(alpha_set)):
            file.write(f"{alpha_set[i]} {solution[i]}\n")

    decoded_text = translate_text(solution)
    with open(decoded_text_file, 'w') as file:
        file.write(decoded_text)

