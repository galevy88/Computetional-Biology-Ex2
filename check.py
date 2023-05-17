
true = {'a': 'y', 'b': 'k', 'c': 'i', 'd': 'n', 'e': 'h', 'f': 'o', 'g': 'x', 'h': 'j', 'i': 's', 'j': 'a', 'k': 'p', 'l': 'l', 'm': 'd', 'n': 'u', 'o': 'b', 'p': 'm', 'q': 't', 'r': 'w', 's': 'c', 't': 'q', 'u': 'r', 'v': 'e', 'w': 'v', 'x': 'g', 'y': 'e', 'z': 'f'}

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
