#!-*-coding:utf-8-*-
from m1z0r3.crypro import *
import time

# ==== Global Variable ====
half_block_len = 4
block_len = 8
dec = "dd67ca82d358f0c8479e118addcec2f8ce086c0f6f239f9b66d7226a38c68198dbd777f366fb9fd83b60d11109be174759c75ea56a4866c2"
num = 16
dec_len = len(dec)
def f(r,n):
    anslist = []
    for i in xrange(half_block_len):
        anslist.append( ( r[i]+n ) % 256 )
    return anslist

def my_xor(a,b):
    anslist = []
    for i in xrange(half_block_len):
        anslist.append(a[i]^b[i])
    return anslist

def round_proc(l,r,n):
    pre_l = r
    pre_r = my_xor(f(r,n),l)
    return pre_l,pre_r

def int_to_hex(a):
    if a<15:
        return "0"+hex(a)[2:]
    else:
        return hex(a)[2:]

def decrypt_block(l,r,n):
    for i in reversed(xrange(2,n+1)):
        # print "i:",i-1
        l,r = round_proc(l,r,i-1)
    # func = lambda x : hex(x)[2:]
    return "".join(map(int_to_hex,l+r))

def main():
    # ==== Local Variable ====
    ans = ""
    block_list = []
    # ==== Prepare ====
    for i in xrange(dec_len):
        ans += dec[i]
        if (i+1) % num == 0:
            block_list.append(ans)
            ans = ""
    print block_list

    # ==== hex_str to int_num ====
    int_block_list = []
    for block in block_list:
        tmp = [int((i+j),16) for (i,j) in zip(block[::2],block[1::2])]
        int_block_list.append(tmp)
    print int_block_list
    print

    # ==== start decrypting! ====
    n = 1
    while True:
        n += 1
        dec_result = ""
        for int_block in int_block_list:
            dec_result += decrypt_block(int_block[4:],int_block[:4],n)
            # print "dec_result:",dec_result
        ans = decode_hex(dec_result)
        if "h4ck" in ans:
            print "Number of round is",n
            print "flag is",ans
            return

if __name__ == '__main__':
    main()