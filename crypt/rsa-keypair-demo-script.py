#rsa-keypair-demo-script.py
# Cheat sheet: 1759 and 691

import math
import random

def isPrime(num):
	num = int(num)
	if num <= 0:
		print('fatal - Negative value passed to isPrime()')
		exit()
	elif num <= 2:
		# I mean... sure, check if 1 or 2 is prime.. I guess...
		return True
	y = 2
	max_factor = math.floor(math.sqrt(num))
	while y <= max_factor:
		if (num % y) == 0:
			return False
		else:
			y += 1
	return True

def findPrime(num,up=False):
	while not isPrime(num):
		if up:
			num += 1
		else:
			num -= 1
	return num

def findRandomPrime(cieling):
	floor_factor = 2
	if cieling > 99_999_999:
		floor_factor = 1000
	floor = int(cieling / floor_factor)
	starter = random.randint(floor,cieling)
	return findPrime(starter)


def is_coprime(a, b):
	while b != 0:
		a, b = b, a % b
	if a == 1:
		return True
	return False

def e_candidate_generator(T):
	# expecting a larger T value than 10
	if T < 100000:
		num = 11
	else:
		num = int(T / 99)
	while num < T:
		yield num
		num += 1


def char_to_int(msg_char):
	return int(msg_char.encode('ascii').hex(),16)


##### RSA DEMO
#   Factoring is hard
#        x * y = 1,215,469
#          What are x and y?
#
#   Hard isn't it?
#   Real RSA uses 2 prime numbers p and q that when multiplied together generate a 
#   2048 bit number that we will call N.
#   For reference, a 2048 bit number is 617 decimal digits long

# In this demo we'll use two smaller but still prime numbers as a demonstration
p = findRandomPrime(100)
q = findRandomPrime(100)
print(f'Our numbers are\n p = {p}\n q = {q}')

# Multiply our p and q together to get N
N = p * q
print(f'\nN is {N}\n')


# In RSA, N serves as a shared part of the encryption/decryption key pairs
#
# In this section we need to find (e) and (d), the two values that will
#    work as the pairs keys in conjunction with N to allow us to encrypt/decrypt
#
# This relies on the mathetical properties of a formula called the Euler Totient
#    The Euler Totient is (p - 1) * (q - 1) and RSA takes advantage of the
#    mathematical relationship this T value has with N to derive our e and d values

# First we will generate our T value:
T = ( p - 1 ) * ( q - 1 )
print(f'\nT is {T}\n')


# Now to find the e and d values.
# 
# Getting e and d is a bit of a process and what we're trying to do is find two values 
# that solve the following equation:
#    ( e * d ) mod T = 1
#
# Basically our two keys, when multiplied together, and divided by our T value must 
#   result in a remainder value of 1 (notice that this 1 is the (-1) from the T formula)
#

# Rules for Finding (e) 
#   1 - Must be less than T
#   2 - Must be co-prime with T and N (no shared factors)
#
#   We'll use a generator to iterate down from T to find potential value(s)

for e_candidate in e_candidate_generator(T):
	if is_coprime(T,e_candidate) and is_coprime(N,e_candidate):
		e = e_candidate
		print(f'Found our e: {e}')
		break

# Now to find (d) we just need to find a value that solves the formula:
#    (e * d) mod T = 1
#
#    RSA actually has rules about how to do this to preserve security but for
#    demonstrating the functionality alone, we're going to just find the 
#    smallest d that works for this demo

for d_candidate in range(e,N):
	if ( e * d_candidate ) % T == 1:
		d = d_candidate
		print(f'Found our d: {d}')


# Recap:
print(f'\n==== Our RSA values:\n p\t{p}\n q\t{q}\n N\t{str(N).ljust(14)} ( p * q )\n T\t{str(T).ljust(14)} ( p - 1 ) * ( q - 1 )\n\n e\t{e}\n d\t{d}')
# And our 'public' and 'private' keys:
print(f'\n=== KeyPairs\nPub : {e},{N}\nPriv: {d},{N}')

# How does it work now?
#   Where m is the message, c is the encrypted message:
#     c = (m ^ e) mod N
#   Then to decrypt use d on the c value instead
#     m = (c ^ d) mod N

# Quick Example
# Ceaser Cipher
# Let "HI" = 89
m = 89
c = (m ** e) % N
print(f'Cipher text of {m}: {c}')

# Decrypting
print(f'Decryption of {c} is {(c ** d) % N}')



##### Little bit bigger demo

# First some functions to change our messages into/out of a list of numbers
def make_msg_list(msg):
	msg_list = []
	for msgchar in msg:
		msg_list.append(ord(msgchar))
	return msg_list

def read_msg_list(msg_list):
	msg = ''
	for msg_ordinal in msg_list:
		msg = f'{msg}{chr(msg_ordinal)}'
	return msg

# Quick demo of the msg<->msg_list
mymsg = "This is a demo"
mymsg_list = make_msg_list(mymsg)
mymsg_rebuilt = read_msg_list(mymsg_list)

print(f'\n== Original Message:\n{mymsg}\n\n== Message as ordinal list:\n{mymsg_list}\n\n== Rebuilt from ordinal list:\n{mymsg_rebuilt}')




###### Okay, quick encryption/decreption functions
def encrypt_msg(msg_list,e,N):
	crypt_msg = []
	for msg_ordinal in msg_list:
		# this msg ordinal to the power of e, then mod N to encrypt it
		# and append to the crypt_msg list
		crypt_msg.append((msg_ordinal ** e) % N)
	return crypt_msg

def decrypt_msg_list(cmsg,d,N):
	msg_list = []
	for cmsg_value in cmsg:
		# Decrypt by taking to power of d, then mod N
		msg_ordinal = (cmsg_value ** d) % N
		msg_list.append(msg_ordinal)
	return msg_list



### Demonstrate a full message encryption:
# Ask for participant input
ourmsg = input("Encrypt me> ")

ourmsg_list = make_msg_list(ourmsg)
ourmsg_cipher = encrypt_msg(ourmsg_list,e,N)

print(f'\n\n== {ourmsg}\nOrdinal List:\n {ourmsg_list}\nCipher List:\n {ourmsg_cipher}\n')

decrypted_list = decrypt_msg_list(ourmsg_cipher,d,N)
print(read_msg_list(decrypted_list))




# What happens if we try to decrypt with the wrong key, say the public key?
decrypted_list = decrypt_msg_list(ourmsg_cipher,e,N)








