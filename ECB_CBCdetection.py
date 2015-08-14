from random import randint
from os import urandom
from ECBmode import encrypt_ECB
from CBCmode import encrypt_CBC
from detectECB import detect_ECB_text
from PKCS7padding import pad, unpad
from hexToBase64 import bytes_to_base64, base64_to_bytes

def rand_key(key_size=16):
    return urandom(key_size)


def pad_rand(text):
    flotsam = bytes_to_base64(urandom(randint(5, 10)))
    jetsam  = bytes_to_base64(urandom(randint(5, 10)))
    return "".join([flotsam, text, jetsam])


def rand_encrypt(key, secret):
    block_size = 16

    secret = pad(pad_rand(secret), block_size)

    if randint(0, 1):
        return encrypt_ECB(key, secret)
    else:
        return encrypt_CBC(key, secret)


def get_encryption_oracle(unknown_string):
    unknown_key = rand_key()
    return lambda s: encrypt_ECB(unknown_key, s + unknown_string)


def get_unknown_bytes(oracle):
    min_ciphertext_length = len(oracle(""))
    prev = min_ciphertext_length
    block_size = -1
    for i in range(min_ciphertext_length):
        l = len(oracle("A"*i))
        if l != prev:
            block_size = l - prev
            break
    assert block_size != -1

    assert detect_ECB_text(oracle("A"*(8*block_size)), block_size)
    uid = randint(0, 128)
    plaintext = ""
    shim_block = "A"*(block_size - 1)
    block_count = min_ciphertext_length/block_size
    for i in range(block_count):
        next_shim = ""
        for j in range(block_size):
            oracle_text = oracle(shim_block)
            target_block = oracle_text[i*block_size:(i+1)*block_size]

            for k in range(256):
                guess = shim_block + next_shim + chr(k)
                result = oracle(guess)[0:block_size]
                if result == target_block:
                    shim_block = shim_block[1:]
                    next_shim += chr(k)
                    break
                    
        plaintext += next_shim
        shim_block = next_shim[1:]

    return plaintext[:-1]

def get_unknown_bytes_with_rand_prefix(nonfuzzed_oracle):
    # Generate our obfuscated oracle
    fuzzed_oracle = lambda s: nonfuzzed_oracle(urandom(randint(0, 512)) + s)

    block_size = 16

    # (For the sake of completeness) verify that the oracle is in ECB mode
    assert detect_ECB_text(fuzzed_oracle("A"*(8*block_size)), block_size)

    marker_block = "B"*(block_size - 1) + "C"
    marker_target = None
    while True:
        result = fuzzed_oracle(marker_block*8)
        blocks = split_into_blocks(result, block_size)
        for i in range(len(blocks) - 8):
            if len(set(blocks[i:i+8])) == 1:
                marker_target = blocks[i]
                break
        if marker_target != None:
            break

    assert marker_target != None
    assert len(marker_target) == block_size


    def defuzzed_oracle(s):
        # Find the marker target, and truncate it and everything before it.
        # This removes the random bytes prepended by the fuzzed oracle.
        while True:
            result = fuzzed_oracle(marker_block + s)
            if marker_target in result:
                target_index = result.index(marker_target)
                return result[target_index + block_size:]

        raise AssertionError("defuzzed_oracle went haywire and somehow returned None.")

    return get_unknown_bytes(defuzzed_oracle)


def split_into_blocks(s, l):
    # s is a string, l is the block size.
    return [s[i*l:(i+1)*l] for i in range(len(s)/l)]


#TODO: This file contains challenges 11, 12, and 14.  Move them to separate files.

def test():
    unknown_string  = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaG"
    unknown_string += "FpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0"
    unknown_string += "IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    unknown_bytes = base64_to_bytes(unknown_string)

    oracle = get_encryption_oracle(unknown_bytes)
    recovered_bytes = get_unknown_bytes(oracle)
    assert recovered_bytes == unknown_bytes

    recovered_bytes = get_unknown_bytes_with_rand_prefix(oracle)
    assert recovered_bytes == unknown_bytes