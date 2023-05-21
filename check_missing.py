from collections import Counter

true = {
    'a': 'y',
    'b': 'x',
    'c': 'i',
    'd': 'n',
    'e': 't',
    'f': 'o',
    'g': 'z',
    'h': 'j',
    'i': 'c',
    'j': 'e',
    'k': 'b',
    'l': 'l',
    'm': 'd',
    'n': 'u',
    'o': 'k',
    'p': 'm',
    'q': 's',
    'r': 'v',
    's': 'p',
    't': 'q',
    'u': 'r',
    'v': 'h',
    'w': 'w',
    'x': 'g',
    'y': 'a',
    'z': 'f'
}


counter = Counter(true.values())

# Values appearing twice or more
duplicates = [letter for letter, count in counter.items() if count > 1]

# Values not appearing at all
all_letters = set("abcdefghijklmnopqrstuvwxyz")
missing = all_letters - set(true.values())

print(f"Duplicate values: {duplicates}")
print(f"Missing values: {missing}")
