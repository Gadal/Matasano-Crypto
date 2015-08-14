from itertools import permutations
from breakRepeatingKeyXOR import hamming_distance

def get_ciphertext():
	with open("detectECB.txt", "r") as datafile:
		return datafile.read().split()


def detect_ECB_function(encryption_function, block_size=16):
	text = encryption_function("YELLOW SUBMARINE", "A"*256)
	return detect_ECB_text(text, block_size)


def detect_ECB_text(text, block_size=16):
	blocks = [text[i:i+block_size] for i in range(0, len(text), block_size)]
	return any(perm[0] == perm[1] for perm in permutations(blocks, 2))


def test():
	lines = []
	for line in get_ciphertext():
		if detect_ECB_text(line):
			lines.append(line)
	assert len(lines) == 1
