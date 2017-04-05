from sage.all import *
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b

X = GF(2).polynomial_ring().gen()

def ntopoly(npoly):
  return sum(c*X**e for e, c in enumerate(Integer(npoly).bits()))

def polyton(poly):
  return sum(int(poly[i])*(1 << i) for i in xrange(poly.degree() + 1))

def p(n):
  return polyton((ntopoly(n)**2)%P)

def str2num(s):
  return int(s.encode('hex'), 16)

def process1(m, k):
    P = 0x100000000000000000000000000000087
    res = 0
    for i in bin(k)[2:]:
        res = res << 1;
        if (int(i)):
            res = res ^^ m
        if (res >> 128):
            res = res ^^ P
    return res

def main():
    ciphertxt = open("ciphertxt","r").read()
    ciphertxt = ciphertxt.strip()
    print ciphertxt
    ciphertxt = ciphertxt.decode("hex")

    P = 0x100000000000000000000000000000087
    A = 0xc6a5777f4dc639d7d1a50d6521e79bfd
    B = 0x2e18716441db24baf79ff92393735345
    known_plain = "One-Time Pad is used here. You won't know that the flag is flag{"


    keys = []
    i = 0
    block_len = 16
    while True:
        if block_len*(i*1)>len(known_plain) or block_len*i>=len(known_plain):
            break
        print known_plain[block_len*i:block_len*(i+1)]
        keys.append(b2l(known_plain[block_len*i:block_len*(i+1)])^^b2l(ciphertxt[block_len*i:block_len*(i+1)]))
        i+=1
    print keys
 
    P = ntopoly(P)
    A_poly = ntopoly(A)
    B_poly = ntopoly(B)
    key0_poly = ntopoly(keys[0])
    key1_poly = ntopoly(keys[1])

    #deno/nume
    #B/(A+1)
    a1_inv = inverse_mod(A_poly+1,P)
    print "a1_inv:",polyton(a1_inv)
    k = process1(B,polyton(a1_inv))
    k_poly = ntopoly(k)

    print k

    deno = key1_poly + k_poly
    nume = key0_poly + k_poly
    print polyton(deno)
    print polyton(nume)
    print polyton(inverse_mod(nume,P))

    AS = process1(polyton(deno),polyton(inverse_mod(nume,P)))
    print AS

    s = 76716889654539547639031458229653027958

if __name__ == '__main__':
    main()
