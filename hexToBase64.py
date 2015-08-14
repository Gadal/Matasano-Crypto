from base64 import *

def hex_to_bytes(hex_str): # 4 bits per character
    return b16decode(hex_str)


def bytes_to_hex(byte_arr):
    return b16encode(byte_arr)


def base64_to_bytes(base64_str): # 6 bits per character
    return b64decode(base64_str)


def bytes_to_base64(byte_arr):
    return b64encode(byte_arr)


def hex_to_base64(hex_str):
    return bytes_to_base64(hex_to_bytes(hex_str))


def base64_to_hex(base64_str):
    return bytes_to_hex(base64_to_bytes(base64_str))


def test():
    hex_str = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d".upper()
    base64_str = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

    hex_bytes = hex_to_bytes(hex_str)
    base64_bytes = base64_to_bytes(base64_str)
    assert hex_bytes == base64_bytes

    hex_to_base64_str = bytes_to_base64(hex_bytes)
    assert hex_to_base64_str == base64_str
    
    base64_to_hex_str = bytes_to_hex(base64_bytes)
    assert base64_to_hex_str == hex_str
    
    hex_to_hex_str = bytes_to_hex(hex_bytes)
    assert hex_to_hex_str == hex_str
    
    base64_to_base64_str = bytes_to_base64(base64_bytes)
    assert base64_to_base64_str == base64_str

    assert hex_str == base64_to_hex(base64_str)
    assert base64_str == hex_to_base64(hex_str)

    assert hex_str == base64_to_hex(hex_to_base64(hex_str))
    assert base64_str == hex_to_base64(base64_to_hex(base64_str))
