from fractions import Fraction,gcd
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b
import socket
import telnetlib
import string
import gmpy

readable = string.ascii_letters+string.digits+string.punctuation

# ======== Interactive shell ========
def shell(s):
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

# ======== Socket Tools ========
def sock(remoteip,remoteport):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((remoteip,remoteport))
    return s, s.makefile('rw',bufsize=0)

def read_until(f, delim='\n'):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data

# ======== Brute Force Template ========
# == Test case : (a,b,c,...,aa,ab,ac,...aaa,aab,aac,...) ==
# import string
# from itertools import product
# def brute_force(rep):
#     for x in product(string.printable, repeat=rep):
#         x = "".join(x)
#         # print x
#         if <conditions>:
#             print x
#             return True
#     print "rep %s is nothing."%rep
#     return False
# def main():
#     for i in xrange(10):
#         if brute_force(i):
#             return
# if __name__ == '__main__':
#     main()

# ======== removing colon and unnecessary character in RSA key format ========
def rsa_param_convert(s):
    s = "".join(s.split())
    s = "".join(s.split(":"))
    return s

# ======== Extended Euclidean algorithm ========
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# ======== mod inverse ========
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
# ======== Generating Secret key of RSA ========
def generate_secret_key(p,q,e):
    phin = (p-1)*(q-1)
    d = egcd(e,phin)[1]
    if d<0:
        return d+phin
    return d


# ======== felmat algorithm ========
# return (p,q)
def isqrt(n):
  x = n
  y = (x + 1 // x) // 2
  while y < x:
    x = y
    y = (x + n // x) // 2
  return x

def fermat(n):
    x = isqrt(n) + 1
    y = isqrt(x * x - n)

    while True:
        w = x * x - n - y * y
        if w == 0:
            break
        elif w > 0:
            y += 1
        else:
            x += 1

    p = x+y
    q = x-y
    print "p=", p
    print "q=", q
    return p, q


# ======== Wiener's Attack ========
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
        return pqlist

    # print "start creating continued fraction list..."
    cflist = continued_fraction(e,n)
    # print cflist
    # print "created continued fraction list."
    # print "start creating (k,d) list..."
    kdlist = calc_cand_kd(cflist)
    # print kdlist
    # print "created (k,d) list"
    # print "start creating (p,q) list..."
    pqlist = calc_cand_pq(e,n,kdlist)
    # print "created (p,q) list."
    return pqlist


# ======== Common Modulus Attack ========
# argument : [["N","e","c"],[n1,e1,c1],[n2,e2,c2]...]
# It allow to give hex and int.
# returning the decrypt text.
def common_modulus_attack(neclist):
    def neclist2int(neclist):
        new_list = []
        for n,e,c in neclist:
            if n =="N":
                continue
            n = int(n[2:].strip("L"),16)
            e = int(e[2:].strip("L"),16)
            c = int(c[2:].strip("L"),16)
            new_list.append([n,e,c])
        return new_list
    if "0x" in neclist[1][0]:
        neclist = neclist2int(neclist)
    for i in xrange(len(neclist)):
        for j in xrange(i+1,len(neclist)):
            e1_tmp = neclist[i][1]
            e2_tmp = neclist[j][1]
            if gcd(e1_tmp,e2_tmp)==1:
                e1 = e1_tmp
                e2 = e2_tmp
                c1 = neclist[i][2]
                c2 = neclist[j][2]
                # print "e1: %d"%(e1)
                # print "e2: %d"%(e2)
                break
    _,a1,a2 = egcd(e1,e2)
    # print _
    # print "a1=%d\n"%(a1)
    # print "a2=%d\n"%(a2)
    # print "c1=%d\n"%(c1)
    # print "c2=%d\n"%(c2)

    # I think that a2 is negative
    if a1<0:
        tmp = a1
        a1 = a2
        a2 = tmp
        tmp = e1
        e1 = e2
        e2 = tmp
        tmp = c1
        c1 = c2
        c2 = tmp

    n = neclist[1][0]
    # print "n=%d"%(n)
    ic2 = modinv(c2,n) # Because we can't calc modinv of negative integer.
    m = ( pow(c1,a1,n)*pow(ic2,-a2,n) ) % n
    return hex(m)[2:-1].decode("hex")


# ======== Chinese Remainder theorem ========
# x = a1 (mod m1)
# x = a2 (mod m2)
# ...
# x = ai (mod mi)
# ...
# x = an (mod mn)
# providing list of [[a1,m1],[a2,m2],...,[ai,mi],...,[an,mn]]
def crt(crtlist):
    def mod_product(crtlist):
        ans = 1
        for _,mod in crtlist:
            ans *= mod
        return ans
    def crt_sum(anslist,M):
        ans = 0
        for x in anslist:
            ans = (ans+x) % M
        return ans
    M = mod_product(crtlist)
    anslist = []
    for a,mod in crtlist:
        x = M/mod # M/mi
        y = modinv(x,mod)
        anslist.append(x*y*a)
    return crt_sum(anslist,M)

# ======== Hastad Broadcast Attack ========
def hba(crtlist,e):
    return gmpy.root(crt(crtlist),e)[0]

# ======== Hex decode ========
def decode_hex(hex_str):
    if len(hex_str)%2 != 0:
        hex_str = "0"+hex_str
    return hex_str.decode("hex")

# ======== split_n ========
# input : split_n("abcdefghijkl",3)
# output: ["abc","def","ghi","jkl"]
def split_n(text, n):
    return [ text[i*n:i*n+n] for i in xrange(len(text)/n) ]

# ======== Caesar Cipher ========
# input : synt 13
# output: flag
def caesar(text,key):
    alpha=string.ascii_lowercase
    ans = ""
    for c in text:
        if c in alpha:
            ans+=alpha[(alpha.index(c)+key)%len(alpha)]
        else:
            ans+=c
    return ans