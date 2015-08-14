from ECB_CBCdetection import rand_key
from PKCS7padding import pad, unpad
from CBCmode import encrypt_CBC, decrypt_CBC

def prepare_userdata(userdata):
	userdata = userdata.replace(";", "%3B").replace("=", "%3D")


def read_userdata(ciphertext):
	decrypted = decrypt_CBC(ciphertext)

def spoof_admin(ciphertext):
	return None

def test():
	unknown_key = rand_key()