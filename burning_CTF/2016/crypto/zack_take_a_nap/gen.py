# coding:utf-8
from random import randint
from fractions import gcd

FLAG = "The Actual Flag Was Here"

def main():
    bits = bin(int(FLAG.encode("hex"), 16))[2:]
    n = len(bits)
    assert(n >= 100)

    w = [randint(10**8, 4 ** n)]
    sn = w[0]
    # 超増加数列の生成
    for i in xrange(1, n):
        w.append(sn + randint(1, 4 ** n))
        sn += w[i]

    with open("w.txt", "wb") as f:
        f.write(", ".join(str(w[i]) for i in xrange(n)))
    
    q = randint(sn+1, sn*2)
    with open("q.txt", "wb") as f:
        f.write(str(q))

    r = randint((q/10**8)+1, q-1)
    while gcd(q, r) != 1:
        r = randint((q/10**8)+1, q-1)

    with open("r.txt", "wb") as f:
        f.write(str(r))

    b = [r * w[i] % q for i in xrange(n)]
    with open("b.txt", "wb") as f:
        f.write(", ".join(str(b[i]) for i in xrange(n)))
    
    c = 0
    for i in xrange(n):
        if bits[i] == "1":
            c += b[i]

    with open("c.txt", "wb") as f:
        f.write(str(c))

if __name__ == "__main__":
    main()
