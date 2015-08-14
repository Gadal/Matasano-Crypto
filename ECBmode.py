from Crypto.Cipher import AES
from PKCS7padding import pad, unpad
from hexToBase64 import base64_to_bytes, bytes_to_base64, bytes_to_hex

def get_ciphertext():
    with open("ECBmode.txt", "r") as datafile:
        return base64_to_bytes(datafile.read().strip())


def encrypt_ECB(key, text, add_padding=True):
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    if add_padding:
        text = pad(text, block_size = len(key))
    ciphertext = cipher.encrypt(text)
    return ciphertext


def decrypt_ECB(key, text, strip_padding=True):
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(text)
    
    # Strip padding when decrypting whole messages.
    # Don't do it if only decrypting a single block.
    if strip_padding:
        return unpad(decrypted)
    else:
        return decrypted


def test():
    key = "YELLOW SUBMARINE"
    encrypted = get_ciphertext()
    decrypted = decrypt_ECB(key, encrypted)
    recrypted = encrypt_ECB(key, decrypted)
    assert encrypted == recrypted
