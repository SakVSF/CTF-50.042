import sys
from Crypto.Util.number import *
import random

# CHANGE THIS: path to your directory
mypath = './utils'
sys.path.insert(0, mypath)
import listener

## Actual group created CTF functions start here
def cipherText(flag, key):
    cipher_text = b''
    t = [ [] for i in range(len(key))]
    for i in range(len(flag)):
      index = ( flag[i] + ord(key[i % len(key)]) ) % 128
      cipher_text += index.to_bytes(1, sys.byteorder)
    return cipher_text

def choose_e_d(p,q):
    phi = (p - 1) * (q - 1)
    d = -1
    while d == -1:
        e = random.getrandbits(128)
        if (GCD(e,phi) !=1):
            continue
        d = inverse(e, phi)
    return e, d

def encrypt_flag():
    # Roll the dice to decide the page
    book_1_pos = random.randint(0,len(book_1)-1)
    book_2_pos = random.randint(0,len(book_1)-1)

    # Choose p and q
    p = book_1[book_1_pos]
    q = book_2[book_2_pos]

    # Choose e and d
    e , d = choose_e_d(p,q)
    n = p * q
    pt = bytes_to_long(CIPHER_FLAG)
    ct = pow(pt, e, n)

    return n, e, ct

book_1 = [int(line.strip()) for line in open('book1.txt', 'r').readlines()]
book_2 = [int(line.strip()) for line in open('book2.txt', 'r').readlines()]

##real flag this will be hidden for the CTF
FLAG = b"fcs22{Pr0f3ss0r_D1nh_T1en_Tu@n_Anh&Ch3n_N1@ngjun}"
KEY = "monkeys"
CIPHER_FLAG = cipherText(FLAG, KEY)

class Challenge():
    def __init__(self):
        self.before_input = "New Challenge\n"

    def challenge(self, your_input):
        if your_input == {"msg": "request"}:
            n, e, ct = encrypt_flag()
            JSON = {"return": f"n: {n}, e: {e}, ct: {ct}"}
            return JSON
        else:
            self.exit = True
            return {"error": "Please request OTP"}

import builtins
builtins.Challenge = Challenge
"""
When you connect, the 'challenge' function will be called on your JSON
input.
"""
listener.start_server(port=13370)
