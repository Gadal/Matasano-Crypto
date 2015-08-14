from uuid import uuid1
from re import sub, match
from ECB_CBCdetection import rand_key
from ECBmode import encrypt_ECB, decrypt_ECB
from PKCS7padding import pad, unpad
from collections import OrderedDict

unknown_key = rand_key()

def decode_cookie(cookie):
	return {x[0]:x[1] for x in [y.split("=") for y in cookie.split("&")]}


def encode_cookie(cookie_dict):
	return "&".join(["=".join([key, cookie_dict[key]]) for key in cookie_dict])


def profile_for(email):
	sanitised_email = sub("[=&]", "", str(email))
	cookie_dict = OrderedDict([("email", sanitised_email),
	    					   ("uid"  , str(uuid1())   ),
							   ("role" , "user"         )])
	return encode_cookie(cookie_dict)


def encrypt_profile(cookie):
	return encrypt_ECB(unknown_key, cookie)


def decrypt_profile(ciphertext):
	return decrypt_ECB(unknown_key, ciphertext)


#This is the only part of the system the attacker can see.
def use_sign_up_form(email): 
	return encrypt_profile(profile_for(email))


def authenticate_admin(token):
	user = decode_cookie(decrypt_profile(token))
	return user["role"] == "admin"


def get_admin_token():
	"""
	Mimicks a sign-up process where you enter an email and get back 
	an AES-ECB-encrypted user token.  You can cut and paste blocks 
	of the user token to construct an admin token.
	"""

	# The eleven \x04 bytes end up getting stripped in unpadding.
	admin = "grbgePrefx" + "admin" + b"\x04"*11 + "@allurbase.com"
	admin_part = use_sign_up_form(admin)

	user_part = use_sign_up_form("padding@gmail.com@gmail.com")
	
	admin_token = user_part[:-16] + admin_part[16:32]
	return admin_token

def test():
	assert decode_cookie("foo=bar&baz=qux&zap=zazzle"            ) == \
						{"foo":"bar", "baz":"qux", "zap":"zazzle"}

	bad_cookie = profile_for("a@b.com&role=admin")
	decoded = decode_cookie(bad_cookie).itervalues()
	assert not any([match("[&=]", v) for v in decoded])

	#profile_for("here@there.com") -->
	#email=here@there.com&uid=2069b4a5-4078-11e5-9035-74d43583f627&role=user

	admin_token = get_admin_token()
	assert authenticate_admin(admin_token)
