# Python 3 Source Code
from base64 import b64encode, b64decode
import sys
import os
import random
from fractions import gcd
from math import sqrt

candi_count = 0
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
encrypted = "a7TFeCShtf94+t5quSA5ZBn4+3tqLTl0EvoMsNxeeCm50Xoet+1fvy821r6Fe4fpeAw1ZB+as3Tphe8xZXQ/s3tbJy8BDzX4vN5svYqIZ96rt35dKuz0DfCPf4nfKe300fM9utiauTe5tgs5utLpLTh0FzYx0O1sJYKgJvul0OfiuTl00BCks+aaJZm8Kwb4u+LtLCqbZ96lv3bieCahtegx+7nzqyO6YCb4b9LovCELZ9Pe0L5rLSaBDzXaftxseAw1JzCF0MGjeCacKb69u9TlgCudZT6Os3ojhcWxD914vNHfeCuaJvH4s4aarBKlGdsT8G4UKZhfJB+y0LbjqCOnZT6baF1WiZeNtfsNtuoo+c=="

def shift(char, key, rev = False):
    if not char in chars:
        return char
    if rev:
        return chars[(chars.index(char) - chars.index(key)) % len(chars)]
    else:
        print((chars.index(char) + chars.index(key)) % len(chars))
        return chars[(chars.index(char) + chars.index(key)) % len(chars)]

def encrypt(message, key):
    encrypted = b64encode(message.encode('ascii')).decode('ascii')
    return ''.join([shift(encrypted[i], key[i % len(key)]) for i in range(len(encrypted))])

def original_decrypt(encrypted, key):
    encrypted = ''.join([shift(encrypted[i], key[i % len(key)], True) for i in range(len(encrypted))])
    return b64decode(encrypted.encode('ascii')).decode('ascii')

# self-made
# not using encode or decode ascii
def decrypt(encrypted, key):
    encrypted = ''.join([shift(encrypted[i], key[i % len(key)], True) for i in range(len(encrypted))])
    return b64decode(encrypted)

def generate_random_key(length = 5):
    return ''.join(map(lambda a : chars[a % len(chars)], os.urandom(length)))

def Kasiski_exam(encrypted):
    strlist = []
    count = 0
    indexlist = []
    for i in range(len(encrypted)):
        for j in range(i,len(encrypted)):
            if j-i<3:
                    continue
            start = i
            search_str = encrypted[i:j]
            while True:
                detect = encrypted[start:].find(search_str)
                if detect == -1:
                    break
                else:
                    count+=1
                    if count==2:
                        strlist.append(search_str)
                        indexlist.append(detect+j-i)
                    start += detect+(j-i)
            if count==0:
                break
            count=0
    print(indexlist)
    print(strlist)
    anslist = my_factor(indexlist)
    return anslist

def my_factor(numlist):
    factor_list = []
    for x in range(2,int(sqrt(numlist[0]))+1):
        if numlist[0]%x == 0 and x>=5 and x<=14:
            factor_list.append(x)
    for i in range(1,len(numlist)):
        anslist = list(factor_list)
        num = numlist[i]
        for x in factor_list:
            if num%x !=0:
                anslist.remove(x)
    return anslist

def is_ascii(string):
    if string:
        for char in string:
            if  char > 126:
                return False
            if char<32 and not char==10:
                return False
    return True

def split_str_and_isascii(plain,num,block):
    start = 3*block
    for i in range(start,len(plain),9):
        if not is_ascii(plain[i:i+num]):
            return False
    return True

# if key_len == 12
def brute_key(encrypted,key_len):
    global candi_count
    candi_key_list = [[],[],[]]
    for block in range(int(key_len/4)):
        for a in chars:
            for b in chars:
                if not split_str_and_isascii(decrypt(encrypted,a+b+"aa"),1,block):
                    continue
                for c in chars:
                    if not split_str_and_isascii(decrypt(encrypted,a+b+c+"a"),2,block):
                        continue
                    for d in chars:
                        if split_str_and_isascii(decrypt(encrypted,a+b+c+d),3,block):
                            candi_key_list[block].append(a+b+c+d)
                            candi_count+=1
    return candi_key_list

#if key_len == 6
def brute_key_6(encrypted,key_len):
    global candi_count
    candi_key_list = []
    for block in range(int(key_len/4)):
        for a in chars:
            for b in chars:
                if not split_str_and_isascii(decrypt(encrypted,a+b+"aa"),1,block):
                    continue
                for c in chars:
                    if not split_str_and_isascii(decrypt(encrypted,a+b+c+"a"),2,block):
                        continue
                    for d in chars:
                        if split_str_and_isascii(decrypt(encrypted,a+b+c+d),3,block):
                            candi_key_list.append(a+b+c+d)
                            candi_count+=1
    return candi_key_list

def main():
    # ==== kasiski examination ====
    factor_list = Kasiski_exam(encrypted) # [6,12]
    print("key_len candidate:",factor_list)
    key_len = factor_list[1]

    # ==== brute force attack to base64 ====
    print("Start brute force...")
    candi_key1,candi_key2,candi_key3 = brute_key(encrypted,key_len)
    print(candi_key1)
    print(candi_key2)
    print(candi_key3)

    # ==== key candidate ====
    keylist = []
    for key1 in candi_key1:
        for key2 in candi_key2:
            for key3 in candi_key3:
                keylist.append(key1+key2+key3)
    print(candi_count)
    print(keylist)

    # if "TWCTF{" in decrypted, It is highly possible that the key is correct.
    for key in keylist:
        dec = decrypt(encrypted,key)
        check = b"TWCTF{"
        if check in dec:
            print("--------- key candidate : decrypted ---------------")
            print(key,":",dec)
            print()

if __name__ == '__main__':
    main()