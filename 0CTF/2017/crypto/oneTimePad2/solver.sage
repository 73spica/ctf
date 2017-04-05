# coding:utf-8
# $ sage -python solver.sage
# sageではべき乗は^でxorは^^だが，元のコードで^が使われているので，-pythonを付けることでpythonの記法に則るようにする．
from sage.all import *
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b

# ===== Sagemathの有限体関連の関数 ====
X = GF(2).polynomial_ring().gen()

def ntopoly(npoly):
  return sum(c*X**e for e, c in enumerate(Integer(npoly).bits()))

def polyton(poly):
  return sum(int(poly[i])*(1 << i) for i in xrange(poly.degree() + 1))

def p(n):
  return polyton((ntopoly(n)**2)%P)

# =====================================

# ===== oneTimePad2.pyからのコピペ =====
def str2num(s):
  return int(s.encode('hex'), 16)

# m * k
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
    s = N
    N = process1(N, N)
    while s:
        if s % 2:
            tmp1 = process2(tmp2, tmp1)
        tmp2 = process2(tmp2, tmp2)
        s = s / 2
    return process1(rand, tmp1[0]) ^ tmp1[1]

# =======================================


# ===== Global Variables =====
P = 0x100000000000000000000000000000087
A = 0xc6a5777f4dc639d7d1a50d6521e79bfd
B = 0x2e18716441db24baf79ff92393735345

# unknown just now.
N = 0

# ===== main =====
def main():
    global N

    ciphertxt = open("ciphertxt","r").read()
    ciphertxt = ciphertxt.strip()
    print "ciphertxt  :", ciphertxt
    ciphertxt = ciphertxt.decode("hex")

    known_plain = "One-Time Pad is used here. You won't know that the flag is flag{"
    print "known_plain:", known_plain

    # key.txtのキーの序盤はknown_plainとciphertxtを16byteごとにxorすることで求められる
    # 最後の1ブロックはフラグが入るため分からない
    keys = []
    i = 0
    block_len = 16
    while True:
        if block_len*(i*1)>len(known_plain) or block_len*i>=len(known_plain):
            break
        keys.append(b2l(known_plain[block_len*i:block_len*(i+1)])^b2l(ciphertxt[block_len*i:block_len*(i+1)]))
        i+=1
    print "keys:"
    print keys
 
    # ===== A^s を求める =====
    # 式変形することで，ASが以下のようになることが分かる
    # A^s = (Key1 + B/(A+1))/(Key0 + B/(A+1))
    # これらはGF(2^128)の元で計算され，生成多項式はP
    print "===== ガロア体の演算 ===== "
    P_poly = ntopoly(P)
    A_poly = ntopoly(A)
    B_poly = ntopoly(B)
    key0_poly = ntopoly(keys[0])
    key1_poly = ntopoly(keys[1])

    #deno/nume
    #B/(A+1)
    a1_inv = inverse_mod(A_poly+1,P_poly) # inverse_mod()はsageの関数
    k = process1(B,polyton(a1_inv))
    k_poly = ntopoly(k)

    print "B/(A+1)",k

    deno = key1_poly + k_poly
    nume = key0_poly + k_poly
    print "key1 + B/(A+1)   :", polyton(deno)
    print "key0 + B/(A+1)   :", polyton(nume)

    AS = process1(polyton(deno),polyton(inverse_mod(nume,P_poly)))
    print "(key1 + B/(A+1)) / (key0 + B/(A+1))  :", AS
    
    # calc from "AS" by using pari/gp 
    # $ gp -q log.gp
    s = 76716889654539547639031458229653027958
    N = s
    key = keys[0]
    ans = ""
    for i in xrange(5):
        ans += l2b(key^b2l(ciphertxt[16*i:16*(i+1)]))
        key = nextrand(key)
    ans += "}"
    print
    print ans
 
if __name__ == '__main__':
    main()
