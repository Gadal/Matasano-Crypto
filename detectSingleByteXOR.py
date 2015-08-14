from singleByteXOR import crack_single_byte_xor

def detect_single_byte_xor(data):
    return max(map(crack_single_byte_xor, data), key=lambda x: x[0])[1] 


def test():
    with open("detectSingleByteXOR.txt", "r") as datafile:
        data = datafile.read().split()
	detect_single_byte_xor(data)
    #print(detect_single_byte_xor(data))
