#!/usr/bin/python

import gmpy
import random
from Crypto.Util import number
import hashlib
import os
from fractions import gcd

flag = '[censored]'

def blumint(r):
    while True:
        p = number.getPrime(r)
        q = number.getPrime(r)
        if (p % 4 == 3) and (q % 4 == 3) and (p != q):
            res = p, q
            break
    return res

def qrn(p, q):
    N = p * q
    while True:
        x = random.randint(1, N)
        if pow(q ** 2 * x, (p-1)/2, p) + pow(p ** 2 * x, (q-1)/2, q) == p + q - 2:
            break
    return x

def goldenmedal(msg, key):
    x, N = key
    imsg = int(msg.encode('hex'), 16) 
    bmsg = bin(imsg)[2:]              
    C = []
    for i in range(0 , len(bmsg)):
        while True:
            y = random.randint(1, N) 
            if gcd(y, N) == 1: 
                b_y = bin(y)[2:] 
                c = (pow(x, int(b_y + bmsg[i], 2), N) * y ** 2) % N 
                C.append(c)
                break
    return C


p, q = blumint(160)
x = qrn(p, q)
N = p * q
key = x, N
enc = goldenmedal(flag, key)
print 'key = ', key 
print 'enc = ', enc
