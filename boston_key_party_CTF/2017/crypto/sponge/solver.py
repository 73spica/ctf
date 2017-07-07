# coding:utf-8
from hash import Hasher, AES
from m1z0r3.crypro import *

def pad(a,l):
    return "\x00"*(l-len(a))

def main():
    aes = AES.new('\x00'*16)
    HASHER = Hasher()
    GIVEN = 'I love using sponges for crypto'
    TARGET = HASHER.hash(GIVEN)
    #print TARGET.encode("hex")
    # 各stateはhash.pyを書き換えて印字すればわかる
    state1 = "49206c6f766520757369000000000000".decode("hex")
    state2 = "b72776391ff42843ffe7cfe6c3d582c6".decode("hex")
    state3 = "cba5d1139c347a3c6fc8afcfecd21a8d".decode("hex")
    state4 = "ef43cd0580d0491c117e7740560a1d64".decode("hex")


    cand_dict = {}
    #memo = 0x5709ff # \x57\x09\xff\x00....で衝突が見つかる

    state = state3
    print "First stap."
    for i in xrange(2**24):
        p2 = l2b(i)
        p2 += pad(p2,16)
        cand = l2b(b2l(p2)^b2l(state))
        cand = pad(cand, 16) + cand
        cand = aes.decrypt(cand)
        cand_dict[cand[10:]] = (i,cand[:10])

    print "Second stap."
    for i in xrange(2**24):
        p0 = l2b(i)
        p0 += pad(p0, 16)
        # こっちはxorする意味なし
        cand = aes.encrypt(p0)
        if cand[10:] in cand_dict:
            tmp = cand_dict[cand[10:]]
            p0 = p0[:10]
            p1 = l2b(b2l(tmp[1])^b2l(cand[:10]))
            c = cand[10:]
            tmp = l2b(tmp[0])
            p2 = tmp + pad(tmp,10)
            p2 = p2[:10]
            print "Detect!!"
            break
    p = p0 + p1 + p2 + "o"
    print "p0:", p0.encode("hex")
    print "p1:", p1.encode("hex")
    print "p2:", p2.encode("hex")
    print "p:",p.encode("hex")
    print "Target:", TARGET.encode("hex")
    print "Result:", HASHER.hash(p).encode("hex")
    assert HASHER.hash(p) == TARGET


if __name__ == "__main__":
    main()
