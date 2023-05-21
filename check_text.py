
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

def get_decode_text(individual, ciphertext):
    # Translate ciphertext using individual mapping
    decoded_text = ""
    for letter in ciphertext:
        if letter in individual:
            decoded_text += individual[letter]
        else:
            decoded_text += letter
    return decoded_text

def get_enc():
    with open('enc.txt', 'r') as f:
        ENC = f.read()
    return ENC

ENC = get_enc()
decode_text= get_decode_text(true, ENC)
print(decode_text)
