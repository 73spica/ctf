from m1z0r3.crypro import *
from Crypto.Util.number import long_to_bytes
import time

def wieners_attack(e,n):
    # calc continued_fraction of x/y
    def continued_fraction(x,y):
        cflist = []
        while True:
            if x==1:
                break
            a = y/x
            b = y%x
            y = x
            x = b
            cflist.append(a)
        return cflist

    def calc_cand_kd(cflist):
        kdlist = []
        for i in xrange(len(cflist)):
            deno = Fraction(cflist[i])
            for j in reversed(xrange(i)):
                b = 1/Fraction(deno)
                a = cflist[j]
                deno = a+b
            kdlist.append([deno.denominator,deno.numerator])
        return kdlist

    def positive_integer_check(a):
        tmp = str(a).split(".")
        if tmp[1]=="0" and ("-" not in tmp[0]):
            return True
        else:
            return False

    def int_sqrt(n):
        def f(prev):
            while True:
                m = (prev + n/prev)/2
                if m >= prev:
                    return prev
                prev = m
        return f(n)

    def calc_cand_pq(e,n,kdlist):
        pqlist = []
        for k,d in kdlist:
            # k = kd[0]
            # d = kd[1]
            if (e*d-1) % k != 0:
                continue
            phin = (e*d-1) / k
            if phin >= n:
                continue
            a = n-phin+1
            b = n
            if a*a < 4*b or a < 0:
                return None
            c = int_sqrt(a*a-4*b)
            p = (a + c) /2
            q = (a - c) /2
            if p + q == a and p * q == b:
                pqlist.append([p,q])
                return d
        return pqlist

    print "start creating continued fraction list..."
    start = time.clock()
    cflist = continued_fraction(e,n)
    # print cflist
    # print "created continued fraction list."
    # print "start creating (k,d) list..."
    kdlist = calc_cand_kd(cflist)
    print time.clock()-start,"s"
    # print kdlist
    # print kdlist
    # print "created (k,d) list"
    # print "start creating (p,q) list..."
    pqlist = calc_cand_pq(e,n,kdlist)
    # print "created (p,q) list."
    return pqlist

def main():
    f = open("intercepted","r")
    i = 0
    dnc = []
    for line in f:
        line = line.strip("{")
        line = line.strip("}\n")
        dnc.append(line.split(":"))
    # print dnc
    d,n,c = map(int,dnc[1])
    e = wieners_attack(d,n)
    dec = pow(c,e,n)
    print dec
    print long_to_bytes(dec)

if __name__ == '__main__':
    main()