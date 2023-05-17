import random
import string

# Constants
POPULATION_SIZE = 3
GENERATIONS = 1000
MUTATION_RATE = 0.01

def get_content():
    # Load dictionary and letter frequencies
    with open("dict.txt", "r") as f:
        DICTIONARY = set([word.strip().lower() for word in f])
        
    FREQ_DICT = {}
    FREQ_2_DICT = {}
    with open("Letter_Freq.txt", "r") as f:
        for line in f:
            freq, letter = line.strip().split()
            FREQ_DICT[letter] = float(freq)
            
    with open("Letter2_Freq.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            parts = line.split()
            if len(parts) != 2:
                continue  # skip lines that don't have 2 parts
            freq, pair = parts
            FREQ_2_DICT[pair] = float(freq)
            
    with open('enc.txt', 'r') as f:
        ENC = f.read()
        
    return DICTIONARY, FREQ_DICT, FREQ_2_DICT, ENC

DICTIONARY, FREQ_DICT, FREQ_2_DICT, ENC = get_content()


def create_population():
    population = []
    for i in range(POPULATION_SIZE):
        individual = {}
        letters = list(string.ascii_lowercase)
        random.shuffle(letters)
        for letter in string.ascii_lowercase:
            individual[letter] = letters.pop()
        population.append(individual)
        # print(f"Gen {i + 1} : {individual}")
    return population


def get_letter_frequency(decoded_text):
    freq_dict = {}
    total_letters = 0
    for letter in decoded_text:
        if letter.isalpha():
            total_letters += 1
            if letter not in freq_dict:
                freq_dict[letter] = 1
            else:
                freq_dict[letter] += 1
    freq_dict = {k: v/total_letters for k, v in freq_dict.items()}
    freq_dict = dict(sorted(freq_dict.items()))
    return freq_dict

def get_letter_pair_frequency(decoded_text):
    freq_dict = {}
    total_pairs = 0
    for i in range(len(decoded_text)-1):
        pair = decoded_text[i:i+2]
        if pair.isalpha():
            total_pairs += 1
            if pair not in freq_dict:
                freq_dict[pair] = 1
            else:
                freq_dict[pair] += 1
    freq_dict = {k: v/total_pairs for k, v in freq_dict.items()}
    freq_dict = dict(sorted(freq_dict.items()))
    return freq_dict

def get_decode_text(individual, ciphertext):
    # Translate ciphertext using individual mapping
    decoded_text = ""
    for letter in ciphertext:
        if letter in individual:
            decoded_text += individual[letter]
        else:
            decoded_text += letter
    return decoded_text
    
def l1_loss(current, original):
    l1_loss = sum(abs(current.get(k.lower(), 0) - original[k]) for k in original) / len(original)
    return l1_loss

def l2_loss(current, original):
    l2_loss = sum((current.get(k.lower(), 0) - original[k]) ** 2 for k in original) / len(original)
    return l2_loss

def fitness(individual, ciphertext):
    print(individual)
    decode_text = get_decode_text(individual, ciphertext)
    current_cipher_freq = get_letter_frequency(decode_text)
    current_cipher_pair_freq = get_letter_pair_frequency(decode_text)

    l1_loss_sole = l1_loss(current_cipher_freq, FREQ_DICT)
    l1_loss_pair = l1_loss(current_cipher_pair_freq, FREQ_2_DICT)
    print(l1_loss_sole)
    print(l1_loss_pair)

    l2_loss_sole = l2_loss(current_cipher_freq, FREQ_DICT)
    l2_loss_pair = l2_loss(current_cipher_pair_freq, FREQ_2_DICT)
    print(l2_loss_sole)
    print(l2_loss_pair)


    


    
    
population = create_population()
for p in population:
    fitness(p, ENC)
