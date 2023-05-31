import numpy as np
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
import sys

word_set = None
char_freqs = None
pair_freqs = None
char_set = np.array(list('abcdefghijklmnopqrstuvwxyz'))
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


def ask_for_file():
    print("Please select your encrypted .txt file")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    if not file_path:
        print("No file selected. Please select a .txt file.")
        sys.exit()

    if not file_path.endswith('.txt'):
        print("Invalid file type. Please select a .txt file.")
        sys.exit()
    
    return file_path


def load_data():
    try:
        encrypted_file_path = ask_for_file()
        
        WORDS = read_words("dict.txt")
        CHAR_FREQ = read_char_freqs("Letter_Freq.txt")
        PAIR_FREQ = read_pair_freqs("Letter2_Freq.txt")
        CIPHERED_TEXT = read_encrypted_text(encrypted_file_path)
        return WORDS, CHAR_FREQ, PAIR_FREQ, CIPHERED_TEXT

    except Exception as e:
        print(str(e))
        return None, None, None, None


DICTIONARY, FREQ, FREQ2, ENC = load_data()
