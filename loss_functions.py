
import Globals as G

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

def zero_one_loss(decode_text):
    words = decode_text.split()
    counter = 0
    for word in words:
        if word in G.DICTIONARY:
            counter+=1
    return 1 - counter/len(G.DICTIONARY)


def l1_loss(current, original):
    l1_loss = sum(abs(current.get(k.lower(), 0) - original[k]) for k in original) / len(original)
    return l1_loss

def l2_loss(current, original):
    l2_loss = sum((current.get(k.lower(), 0) - original[k]) ** 2 for k in original) / len(original)
    return l2_loss

def fitness(individual, ciphertext, loss, type):
    individual_dict = individual.dictonary
    decode_text = get_decode_text(individual_dict, ciphertext)
    
    if(loss == zero_one_loss):
        return zero_one_loss(decode_text)
    
    else:
        if(type != 'pair'):
            current_cipher_freq = get_letter_frequency(decode_text)
            loss_sole = loss(current_cipher_freq, G.FREQ_DICT)
            return loss_sole
        else:
            current_cipher_pair_freq = get_letter_pair_frequency(decode_text)
            loss_pair = loss(current_cipher_pair_freq, G.FREQ_2_DICT)
            return loss_pair


