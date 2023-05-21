import Globals as G
import numpy as np

alpha_set = np.array(list('abcdefghijklmnopqrstuvwxyz'))

def translate_text(code):
    mapping = dict(zip(alpha_set, code))
    dec_text = G.ENC.translate(str.maketrans(mapping))
    return dec_text

def fitness(code):
    G.COUNTER+=1
    plain_text = translate_text(code)
    score = 0.0

    for char in plain_text:
        score += G.FREQ[char]

    text_words = plain_text.lower().split()
    for word in text_words:
        if word in G.DICTIONARY:
            score += 1.0

    for i in range(len(plain_text) - 1):
        char_pair = plain_text[i:i + 2]
        score += G.FREQ2[char_pair]*10

    return score
