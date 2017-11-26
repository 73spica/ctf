# coding:utf-8
from m1z0r3.crypro import sock, read_until, l2b
from fractions import Fraction

remoteip = "localhost"
remoteip = "13.113.218.1"
remoteport = 12345

s,f = sock(remoteip, remoteport)

def get_flag():
    read_until(f, "> ")
    s.send("3")
    read_until(f) # You selected 3.
    enc_flag = eval(read_until(f).split(":")[-1])
    return enc_flag

def get_pk():
    read_until(f, "> ")
    s.send("4")
    read_until(f) # You selected 4.
    pk = eval(read_until(f).split(":")[-1])
    return pk

def get_lsb(cipher):
    c1, c2 = cipher
    read_until(f, "> ")
    s.send("2")
    read_until(f) # You selected 2.
    read_until(f, ": ")
    s.send(str(c1))
    read_until(f, ": ")
    s.send(str(c2))
    lsb = int(read_until(f).strip())
    print lsb
    return lsb
    
def get_enc(msg):
    read_until(f, "> ")
    s.send("1")
    read_until(f) # You selected 1.
    read_until(f, ": ")
    s.send(str(msg))
    c = eval(read_until(f).strip())
    return c

def cipher_product(c1,c2,p):
    return (c1[0]*c2[0] % p, c1[1]*c2[1] % p)

def main():
    print "==== Flag cipher ===="
    enc_flag = get_flag()
    print enc_flag

    print "==== Decryption Test ===="
    print get_lsb(enc_flag)
    y,g,p = get_pk()

    print "==== Public Key ===="
    print "p:",p
    print "y:",y
    print "g:",g

    print "==== Encryption Test ===="
    c = get_enc("hoge")
    print "c:",c

    # LSB Oracle Attack for Elgamal Oracle
    print "==== LSB Oracle Attack for ElGamal Oracle ===="
    lb = 0
    ub = Fraction(p) 
    send_cipher = enc_flag
    i = 0
    enc_2 = get_enc("\x02")
    enc_2i = (1,1)
    while True:
        enc_2i = cipher_product(enc_2i, enc_2, p)
        send_cipher = cipher_product(enc_flag, enc_2i, p)
        lsb = get_lsb(send_cipher)
        i+=1
        if lsb:
            lb = (lb+ub)/2
        else:
            ub = (lb+ub)/2
        diff = ub - lb
        diff = diff.numerator / diff.denominator
        if diff == 0:
            m = ub.numerator / ub.denominator
            break
    print "==== Attack Result ===="
    print "[+] m:", m
    print
    print "[+] Flag:",l2b(m)
    print
    print "[+] Num. of requests:",i


    s.close()
    f.close()



if __name__ == "__main__":
    main()
