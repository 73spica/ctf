from m1z0r3.crypro import *
from math import sqrt
import time

def do_calc(num):
    span = 2
    b = 1
    if num%2==0:
        a = 2
    elif str(num)[-1]=="5":
        a = 5
        span = 5
    else:
        a = 3
    detect_f = False
    while True:
        if detect_f:
            break
        b=1
        while True:
            ans = a**b
            if ans > num:
                # print "none.",a
                break
            if ans == num:
                print "[+] complete!!"
                print "[+] a = %s , b = %s"%(a,b)
                return a,b
            b+=1
            # print ans
        a+=span

def main():
    remoteip = "ctf.com.ua"
    remoteport = 9988
    s,f = sock(remoteip,remoteport)

    for i in xrange(100):
        print "[+] stage%s"%i
        data = read_until(f,"C =  ")
        num = read_until(f)
        print "[+]",num
        a,b = do_calc(int(num))
        ans = "%s %s\n"%(a,b)
        print "send:",ans
        s.send(ans)
    shell(s) # h4ck1t{R4ND0M_1S_MY_F4V0UR1T3_W34P0N}

    f.close()
    s.close()

if __name__ == '__main__':
    main()