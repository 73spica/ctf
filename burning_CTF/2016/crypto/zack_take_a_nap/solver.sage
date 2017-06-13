# -*- coding: utf-8 -*-
# lazyの時と同じsolver
from sage.all import *
from Crypto.Util.number import long_to_bytes as l2b

def main():
    # 各種値の読み込み
    pub = eval(open("b.txt","r").read())
    cipher = int(open("c.txt","r").read())
    N = len(pub)
    print "N:",N
    print "max(pub):",max(pub)
    d = N / n(log(max(pub),2))
    print d
    l = long(n(sqrt(N)) *2)
    print "l:",l

    # 格子を作っていく．ここではCLOS法を用いる
    # N行N列の単位行列
    x = matrix.identity(N)
    x = 2*x
    tmp = [long(-1) for i in xrange(N)]
    tmp = matrix(ZZ,1,N,tmp)
    m = x.stack(tmp)

    tmp2 = []
    for i in xrange(N):
        tmp2.append(-2*l*pub[i])

    tmp2.append(2*l*cipher)
    tmp2 = matrix(ZZ,N+1,1,tmp2)
    m = m.augment(tmp2)
    #print m.str()

    lllm = m.LLL()
    #print lllm.str()

    for row in lllm.rows():
        detect = True
        if row[-1]!=0:
            continue
        for num in row[:-1]:
            if num != 1 and num != -1:
                detect = False
                break
        if detect:
            print "detect!!!!"
            ans_row = row[:-1]
            break
    if not detect:
        print "nothing"
    print ans_row

    ans_bin = ""
    for b in ans_row:
        if b==1:
            ans_bin+="1"
        elif b==-1:
            ans_bin+="0"
        else:
            print "おかしいやで"

    print ans_bin
    print l2b(int(ans_bin,2))
    print l2b(int(ans_bin[::-1],2))


if __name__ == "__main__":
    main()
