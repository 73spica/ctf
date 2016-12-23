# -*- coding: utf-8 -*-

# I forgot the question...

def split_str(s, n):
    "split string by its length"
    length = len(s)
    return [s[i:i+n] for i in range(0, length, n)]

def main():
    f = open('4042.txt', 'r')
    utf9 = ""
    for line in f:
        utf9 += line.strip()
    utf9bin = bin(int(utf9,8))[2:]
    utf9binlist = split_str(utf9bin,9)
    print utf9binlist
    # anslist = []
    # for x in xrange(0,len(utf9binlist)-1):
    #     if utf9binlist[x][0] == utf9binlist[x+1][0] and utf9binlist[x][0]=="0" :
    #         anslist.append(utf9binlist[x+1])
    # decode
    # ans = ""
    # print anslist[0][1:]
    # for x in xrange(0,len(anslist)):
    #     ans += chr(int(anslist[x][1:],2))
    # print ans
    tmpstr = ""
    ans =""
    for x in xrange(0,len(utf9binlist)):
        if utf9binlist[x][0]=="1":
            tmpstr += utf9binlist[x][1:]
        elif utf9binlist[x][0] == "0":
            tmpstr += utf9binlist[x][1:]
            ans += unichr(int(tmpstr,2))
            tmpstr = ""
    print ans


if __name__ == '__main__':
    main()
