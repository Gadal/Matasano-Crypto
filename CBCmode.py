from PKCS7padding import pad, unpad
from fixedXOR import fixed_xor
from ECBmode import encrypt_ECB, decrypt_ECB
from hexToBase64 import base64_to_bytes, bytes_to_base64

def generate_blocks(text, block_size):
    assert len(text) % block_size == 0
    return [text[i:i+block_size] for i in range(0, len(text), block_size)]


def encrypt_CBC(key, text):
    block_size = 16
    
    text_blocks = generate_blocks(pad(text), block_size)
    initialisation_vector = b'\x00' * block_size

    cipher_blocks = [initialisation_vector]
    for i in range(len(text_blocks)):
        xor = fixed_xor(cipher_blocks[i], text_blocks[i])
        cipher_blocks.append(encrypt_ECB(key, xor, add_padding=False))

    return "".join(cipher_blocks[1:])


def decrypt_CBC(key, text):
    block_size = 16

    cipher_blocks = generate_blocks(text, block_size)
    initialisation_vector = b'\x00' * block_size
    cipher_blocks.insert(0, initialisation_vector)
    
    text_blocks = []

    for i in range(len(cipher_blocks) - 1):
        decrypted = decrypt_ECB(key, cipher_blocks[i + 1], strip_padding=False)
        text_blocks.append(fixed_xor(cipher_blocks[i], decrypted))

    return unpad("".join(text_blocks))


def test():
    key = "YELLOW SUBMARINE"#.encode("utf-8")
    
    text = "ABCD"*64
    encrypted = encrypt_CBC(key, text)
    decrypted = decrypt_CBC(key, encrypted)
    assert decrypted == text

    with open("CBCmode.txt", "r") as datafile:
        text = base64_to_bytes(datafile.read().strip())
    decrypted = decrypt_CBC(key, text)
    recrypted = encrypt_CBC(key, decrypted)
    assert recrypted == text
