from fixedXOR import fixed_xor
from hexToBase64 import hex_to_bytes
from itertools import permutations

def crack_single_byte_xor(text):
    return single_byte_xor(infer_key(text), text)


def single_byte_xor(key, text):
    return fixed_xor(key*len(text), text)


def infer_key(text):
    perms = [hex_to_bytes("".join(p)) for p in list(permutations("0123456789ABCDEF", 2))]
    return max(map(lambda xor: (score(xor, text), xor), perms), key=lambda x: x[0])[1]


def score(key, text):
    freqs = { "a": 0.08167, "b": 0.01492, "c": 0.02782, "d": 0.04253, "e": 0.12702, "f": 0.02228,
              "g": 0.02015, "h": 0.06094, "i": 0.06966, "j": 0.00153, "k": 0.00772, "l": 0.04025,
              "m": 0.02406, "n": 0.06749, "o": 0.07507, "p": 0.01929, "q": 0.00095, "r": 0.05987,
              "s": 0.06327, "t": 0.09056, "u": 0.02758, "v": 0.00978, "w": 0.02360, "x": 0.00150,
              "y": 0.01974, "z": 0.00074 }

    result = single_byte_xor(key, text)
    return 1/sum([abs(freqs[l] - (result.count(l)/float(len(result)))) for l in freqs.keys()])


def test():
    ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736".upper()
    hex_bytes = hex_to_bytes(ciphertext)
    crack_single_byte_xor(hex_bytes)
    #print(crack_single_byte_xor(hex_bytes)) # solution: "Cooking MC's like a pound of bacon"
