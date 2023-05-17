

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
