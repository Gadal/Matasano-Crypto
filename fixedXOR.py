from hexToBase64 import hex_to_bytes

def fixed_xor(bytes1, bytes2):
    assert len(bytes1) == len(bytes2)
    return "".join([chr(ord(x)^ord(y)) for x, y in zip(bytes1, bytes2)])


def test():
    t1 = "1c0111001f010100061a024b53535009181c".upper()
    t2 = "686974207468652062756c6c277320657965".upper()
    r  = "746865206b696420646f6e277420706c6179".upper()

    assert fixed_xor(hex_to_bytes(t1), hex_to_bytes(t2)) == hex_to_bytes(r)
