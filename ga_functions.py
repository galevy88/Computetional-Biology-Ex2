import numpy as np
import Globals
import random
import string

def fill_miss_values(c):
    letters = set(string.ascii_lowercase)
    missing_letters = letters - set(c.dictonary.values())

    duplicates = [v for v in c.dictonary.values() if list(c.dictonary.values()).count(v) > 1]
    keys_with_duplicates = [k for k, v in c.dictonary.items() if v in duplicates]

    # Fill missing letters
    for letter in missing_letters:
        key = keys_with_duplicates.pop(0)
        c.dictonary[key] = letter

    return c
    

def crossover(p1, p2, update_vec):
    c1 = p1.deepcopy()
    c2 = p2.deepcopy()
    alpha = [random.choice(update_vec) for _ in range(len(p1.dictonary))]

    # Swap letters between p1 and p2 based on alpha
    for i, swap in enumerate(alpha):
        if swap == 1:
            # Swap the corresponding letters in the dictionaries
            key1 = list(p1.dictonary.keys())[i]
            key2 = list(p2.dictonary.keys())[i]
            value1 = p1.dictonary[key1]
            value2 = p2.dictonary[key2]
            c1.dictonary[key1] = value2
            c2.dictonary[key2] = value1
            
    fill_miss_values(c1)
    fill_miss_values(c2)

    return c1, c2


def mutate(x, mu):
    y = x.deepcopy()
    keys = list(y.dictonary.keys())
    flag = np.random.rand(len(keys)) <= mu
    ind = np.argwhere(flag).flatten()

    # Iterate over the indices where mutation should occur
    for idx in ind:
        letter = keys[idx]
        different_letter = random.choice([l for l in string.ascii_lowercase if l != y.dictonary[letter]])
        y.dictonary[letter] = different_letter

    fill_miss_values(y)
    return y




def roulette_wheel_selection(p):
    c = np.cumsum(p)
    r = sum(p)*np.random.rand()
    ind = np.argwhere(r <= c)
    return ind[0][0]

def print_top_5(bestsol, pop, it):
        print(f"First Solution : {bestsol.dictonary}")
        print(f"Second Solution: {pop[1].dictonary}")
        print(f"Third  Solution: {pop[2].dictonary}")
        print(f"Fourth Solution: {pop[3].dictonary}")
        print(f"Fifth  Solution: {pop[4].dictonary}")
        print("Iteration {}: First  Cost = {}".format(it, bestsol.cost))
        print("Iteration {}: Second Cost = {}".format(it, pop[1].cost))
        print("Iteration {}: Third  Cost = {}".format(it, pop[2].cost))
        print("Iteration {}: Fourth Cost = {}".format(it, pop[3].cost))
        print("Iteration {}: Fifth  Cost = {}".format(it, pop[4].cost))
        
def get_top_5(bestsol, pop):
    top_5 = [bestsol] + pop[1:5]
    return [sol.dictonary for sol in top_5], [sol.cost for sol in top_5]


def remove_duplicates(objects):
    unique_objects = []
    seen_dictionaries = set()

    for obj in objects:
        dictionary = obj.dictonary
        dictionary_tuple = tuple(sorted(dictionary.items()))

        if dictionary_tuple not in seen_dictionaries:
            unique_objects.append(obj)
            seen_dictionaries.add(dictionary_tuple)

    return unique_objects

