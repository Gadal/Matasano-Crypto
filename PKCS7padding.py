def pad(text, block_size=16):
	if block_size > 255:
		raise ValueError("block_size > 255")

	pad_length = block_size - (len(text) % block_size)

	if pad_length == 0:
		pad_length = block_size
	return text + chr(pad_length)*pad_length


def unpad(text):
	if len(text) == 0:
		raise ValueError("Attempted to unpad zero-length string")
	pad_char = text[-1]
	pad_length = ord(pad_char)
	padding = text[-pad_length:]

	if len(padding) < pad_length:
		raise ValueError("Invalid padding.  Padding too short.")

	for char in padding:
		if char == pad_char:
			continue

		raise ValueError("Invalid padding.  Unexpected padding character.")

	return text.rstrip(pad_char)
