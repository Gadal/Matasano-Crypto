from singleByteXOR import infer_key, single_byte_xor
from repeatingKeyXOR import repeating_key_xor
from hexToBase64 import base64_to_hex, hex_to_base64, base64_to_bytes, bytes_to_base64, bytes_to_hex
from itertools import permutations

def get_ciphertext():
    with open("breakRepeatingKeyXOR.txt", "r") as datafile:
        return datafile.read().strip()

def hamming_distance(s0, s1):
    return sum(map(lambda a, b: len([i for i in range(8) if (ord(a)^ord(b))&(2**i) != 0]), *[s0, s1]))

def guess_keysize(text):
    ave_distances = []
    start = 1
    end = 40
    for i in range(start, end):
        blocks_at_i = [text[j*i:j*i + i] for j in range(len(text)/i)]
        cap = 16
        if len(blocks_at_i) > cap:
            blocks_at_i = blocks_at_i[:cap]

        block_perms = permutations(blocks_at_i, 2)
        ave_dist = sum([hamming_distance(p[0], p[1]) for p in block_perms])/float(len([block_perms]))
        ave_distances.append((i, ave_dist))

    anomalies = [] # All else being equal, one would expect the average hamming distance to increase.
    for i in range(start + 1, end - 2):
        if ave_distances[i][1] < ave_distances[i - 1][1]:
            anomalies.append(ave_distances[i])
            ave_distances.pop(i)

    ret =      sorted(anomalies,     key=lambda x: x[1])
    ret.extend(sorted(ave_distances, key=lambda x: x[1]))
    ret = [x[0] for x in ret]
    return ret

def decrypt_repeating_key(text):
    keysize = guess_keysize(text)[0]

    block_count = len(text)/keysize
    block_size = keysize
    blocks = [[text[i*block_size+j] for i in range(block_count)] for j in range(block_size)]
    blocks = ["".join(block) for block in blocks]

    key = "".join([infer_key(block) for block in blocks])

    return repeating_key_xor(key, text)

def test():
    s0 = "this is a test"
    s1 = "wokka wokka!!!"
    assert hamming_distance(s0, s1) == 37

    text = base64_to_bytes(get_ciphertext())
    result = decrypt_repeating_key(text)
    #print(result)
