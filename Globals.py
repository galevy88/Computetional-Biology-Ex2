import numpy as np
from collections import defaultdict


word_set = None
char_freqs = None
pair_freqs = None
char_set = np.array(list('abcdefghijklmnopqrstuvwxyz'))
encrypted_file = "enc.txt"
result_text_file = "deciphered.txt"
optimal_code_file = "optimal.txt"
ciphered_text = ""

COUNTER = 0


def read_words(file_path):
    with open(file_path, 'r') as file:
        words = set(word.strip().lower() for word in file)
    return words


def read_char_freqs(file_path):
    with open(file_path, 'r') as file:
        freqs = defaultdict(float)
        for line in file:
            values = line.strip().split('\t')
            if len(values) == 2:
                freq, char = values
                freqs[char.lower()] = float(freq)
    return freqs


def read_pair_freqs(file_path):
    with open(file_path, 'r') as file:
        freqs = defaultdict(float)
        for line in file:
            values = line.strip().split('\t')
            if len(values) == 2:
                freq, pair = values
                freqs[pair.lower()] = float(freq)
    return freqs


def read_encrypted_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read().lower()
    return text


def load_data():
    WORDS = read_words('dict.txt')
    CHAR_FREQ = read_char_freqs('Letter_Freq.txt')
    PAIR_FREQ = read_pair_freqs('Letter2_Freq.txt')
    CIPHERED_TEXT = read_encrypted_text('enc.txt')
    return WORDS, CHAR_FREQ, PAIR_FREQ, CIPHERED_TEXT


DICTIONARY, FREQ, FREQ2, ENC = load_data()

