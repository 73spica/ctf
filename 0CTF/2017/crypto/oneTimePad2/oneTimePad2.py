#!/usr/bin/env python
# coding=utf-8

from os import urandom
from m1z0r3.crypro import *

# 今度は掛け算してるだけ？
def process1(m, k):
    res = 0
    for i in bin(k)[2:]:
        res = res << 1;
        if (int(i)):
            res = res ^ m
        if (res >> 128):
            res = res ^ P
    return res

# ベクトル同士の積
def process2(a, b):
    res = []
    res.append(process1(a[0], b[0]) ^ process1(a[1], b[2]))
    res.append(process1(a[0], b[1]) ^ process1(a[1], b[3]))
    res.append(process1(a[2], b[0]) ^ process1(a[3], b[2]))
    res.append(process1(a[2], b[1]) ^ process1(a[3], b[3]))
    return res

def nextrand(rand):
    global N, A, B
    tmp1 = [1, 0, 0, 1]
    tmp2 = [A, B, 0, 1]
    s = N # 乱数．randが分かれば逆算可能．どんどんN^2された値になっていく．
    N = process1(N, N) # rand0の2乗．どんどん2乗されてく．
    while s: # sが0でない間
        if s % 2: # 偶数なら
            tmp1 = process2(tmp2, tmp1)
        tmp2 = process2(tmp2, tmp2)
        s = s / 2
    return process1(rand, tmp1[0]) ^ tmp1[1] # randは分からないが

def keygen():
    key = str2num(urandom(16))
    key = 88759977654662465230648243503936608956L
    while True:
        yield key
        key = nextrand(key)

def encrypt(message):
    length = len(message)
    pad = '\x00' + urandom(15 - (length % 16)) # 1ブロック16文字となるようパディング
    to_encrypt = message + pad
    res = ''
    generator = keygen()
    f = open('key.txt', 'w') # This is used to decrypt and of course you won't get it.
    for i, key in zip(range(0, length, 16), generator):
        f.write(hex(key)+'\n')
        res += num2str(str2num(to_encrypt[i:i+16]) ^ key)
    f.close()
    return res

def decrypt(ciphertxt):
    # TODO

    pass

def str2num(s):
    return int(s.encode('hex'), 16)

def num2str(n, block=16):
    s = hex(n)[2:].strip('L')
    s = '0' * ((32-len(s)) % 32) + s
    return s.decode('hex')

P = 0x100000000000000000000000000000087
A = 0xc6a5777f4dc639d7d1a50d6521e79bfd
B = 0x2e18716441db24baf79ff92393735345
N = str2num(urandom(16))
N = 76716889654539547639031458229653027958
assert N != 0


def main():
    key = 88759977654662465230648243503936608956L
    ciphertxt = open('ciphertxt',"r").read().strip()
    print ciphertxt
    ciphertxt = ciphertxt.decode("hex")
    for i in xrange(5):
        print l2b(key^b2l(ciphertxt[16*i:16*(i+1)]))
        key = nextrand(key)
        print key

if __name__ == '__main__':
    main()
    # [88759977654662465230648243503936608956L, 235546735134270273752058597439343181239L, 38897548254986938853913575127240042830L, 55241375418437046672956208930754451536L]
    # with open('top_secret') as f:
    #     top_secret = f.read().strip()
    # assert len(top_secret) == 16
    # plain = "One-Time Pad is used here. You won't know that the flag is flag{%s}." % top_secret

    # with open('ciphertxt', 'w') as f:
    #     f.write(encrypt(plain).encode('hex')+'\n')
