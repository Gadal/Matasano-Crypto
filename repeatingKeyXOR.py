from fixedXOR import fixed_xor
from hexToBase64 import bytes_to_hex, bytes_to_base64

def repeating_key_xor(key, text):
    return "".join([fixed_xor(text[i], key[i%len(key)]) for i in range(len(text))])


def test():
    key = "ICE"
    secret =  "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    target =  "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632427276527".upper()
    target += "2a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f".upper()
    
    assert bytes_to_hex(          repeating_key_xor(key, secret)) == target
    assert repeating_key_xor(key, repeating_key_xor(key, secret)) == secret
