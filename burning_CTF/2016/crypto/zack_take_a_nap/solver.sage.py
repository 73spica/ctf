# -*- coding: utf-8 -*-

# This file was *autogenerated* from the file solver.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0)
from sage.all import *
from Crypto.Util.number import long_to_bytes as l2b

def main():
# 各種値の読み込み
    pub = eval(open("b.txt","r").read())
    cipher = int(open("c.txt","r").read())
    N = len(pub)
#max_pub_bits = len(bin(max(pub))[2:])
    print "N:",N
    print "max(pub):",max(pub)
    d = N / n(log(max(pub),_sage_const_2 ))
    print d
    l = long(n(sqrt(N)) *_sage_const_2 )
    print "l:",l
# N行N列の単位行列
    x = matrix.identity(N)
    x = _sage_const_2 *x
    tmp = [long(-_sage_const_1 ) for i in xrange(N)]
    tmp = matrix(ZZ,_sage_const_1 ,N,tmp)
    m = x.stack(tmp)

    tmp2 = []
    for i in xrange(N):
        tmp2.append(-_sage_const_2 *l*pub[i])

    tmp2.append(_sage_const_2 *l*cipher)
    tmp2 = matrix(ZZ,N+_sage_const_1 ,_sage_const_1 ,tmp2)
    m = m.augment(tmp2)
#print m.str()

    lllm = m.LLL()
#print lllm.str()

    for row in lllm.rows():
        detect = True
        if row[-_sage_const_1 ]!=_sage_const_0 :
            continue
        for num in row[:-_sage_const_1 ]:
            if num != _sage_const_1  and num != -_sage_const_1 :
                detect = False
                break
        if detect:
            print "detect!!!!"
            ans_row = row[:-_sage_const_1 ]
            break
    if not detect:
        print "nothing"
    print ans_row

    ans_bin = ""
    for b in ans_row:
        if b==_sage_const_1 :
            ans_bin+="1"
        elif b==-_sage_const_1 :
            ans_bin+="0"
        else:
            print "おかしいやで"

    print ans_bin
    print l2b(int(ans_bin,_sage_const_2 ))
    print l2b(int(ans_bin[::-_sage_const_1 ],_sage_const_2 ))
# matrix(ZZ,x行,y列,元データ):リストとかを行列に変換
# x.stack(y):xをyに積む
#m = x.stack(matrix(ZZ,1,n,y))
# x.augment(y):xの右にyをくっつける
#m = m.augment(matrix(ZZ,n+1,1,y))

# 行列の列を取り出す(iterable) 
#m.rows()

# LLLアルゴリズムにより最短ベクトルっぽいものを導出
#lllm = m.LLL()

if __name__ == "__main__":
    main()
