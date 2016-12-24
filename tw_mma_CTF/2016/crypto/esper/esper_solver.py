import hashlib
import telnetlib
from m1z0r3.crypro import *
from fractions import gcd
# nc cry1.chal.ctf.westerns.tokyo 37992
# https://score.ctf.westerns.tokyo/problems/14?locale=ja
# TWCTF{I_don't_Lik3_ESPer_problems!}


def proof_of_works(start,end):
    number = start
    while True:
        if number>end:
            break
        if(hashlib.sha1(str(number)).hexdigest().startswith("00000")):
            # print number
            break
        number+=1
    return number
def shell(s):
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()
def main():

    e = 65537
    remoteip = "cry1.chal.ctf.westerns.tokyo"
    remoteport = 37992
    s,f = sock(remoteip,remoteport)
    read_until(f).strip() # proof of works
    read_until(f,"true and ").strip()

    # Get start number
    data = read_until(f," <= number <= ").strip()
    start = data.split()[0]

    # Get end number
    data = read_until(f).strip()
    end = data

    ans = str(proof_of_works(int(start),int(end)))
    print "[+] ans is %s"%ans
    s.send(ans+"\n")

    shell(s)

    data = read_until(f,">").strip()
    print data

    # show n

    ## 2
    s.send("1\n") # choice
    data = read_until(f,"string:").strip()
    print data
    s.send("hey\n")
    data = read_until(f,"m:").strip()
    print data
    s.send("2\n")
    data = read_until(f,"Encrypted: ").strip()
    data = read_until(f,">").strip()
    print data
    tmp2 = data.split()[0]
    # print "tmp2:",tmp2

    ##3
    s.send("1\n") # choice
    data = read_until(f,"string:").strip()
    print data
    s.send("hey\n")
    data = read_until(f,"m:").strip()
    print data
    s.send("3\n")
    data = read_until(f,"Encrypted: ").strip()
    data = read_until(f,">").strip()
    print data
    tmp3 = data.split()[0]
    # print "tmp3:",tmp3

    ##4
    s.send("1\n") # choice
    data = read_until(f,"string:").strip()
    print data
    s.send("hey\n")
    data = read_until(f,"m:").strip()
    print data
    s.send("4\n")
    data = read_until(f,"Encrypted: ").strip()
    data = read_until(f,">").strip()
    print data
    tmp4 = data.split()[0]
    tmp2 = int(tmp2)
    tmp3 = int(tmp3)
    tmp4 = int(tmp4)

    print "[+] tmp2:",tmp2
    print "[+] tmp3:",tmp3
    print "[+] tmp4:",tmp4
    e2 = 2**e
    e3 = 3**e
    e4 = 4**e

    n = gcd((e2-tmp2),(e3-tmp3))
    print "[+] n:",n
    n = gcd((e2-tmp2),(e4-tmp4))
    print "[+] n:",n

    # p
    # s.send("2\n") # choice
    # data = read_until(f,"string:").strip()
    # print data
    # s.send("hey\n") # esper
    # data = read_until(f,"c:").strip()
    # print data
    # # print str(tmp2)
    # s.send(str(tmp2)+"\n") # c
    # data = read_until(f,"Decrypted:").strip()
    # data = read_until(f,">").strip()
    # print data
    # m_a = data.split()[0]
    # print "[+] m_a:",m_a

    s.send("2\n") # choice
    data = read_until(f,"string:").strip()
    print data
    s.send("7:m2\n") # esper
    data = read_until(f,"c:").strip()
    print data
    s.send(str(tmp2)+"\n") # c
    data = read_until(f,":").strip()
    print data
    data = read_until(f,"\n").strip()
    print data
    m_a = int(data)
    print "[+] m_a:",m_a

    p = gcd(n,m_a-2)
    q = n/p
    print "[+] p:",p
    print "[+] q:",q

    # data = read_until(f,">").strip()
    data = s.recv(1024)
    print data
    data = s.recv(1024)
    print data
    flag_enc = data.split("\n")[1]
    print flag_enc
    d = generate_secret_key(p,q,e)
    flag_dec = pow(int(flag_enc),d,n)
    flag = hex(flag_dec)[2:-1].decode("hex")
    print flag
    # data = s.recv(1024)
    # print data


if __name__ == '__main__':
    main()
    # ans = proof_of_works(70184995772865988401893089559547834719233766229057499219805339844338305705856,70184995772865988401893089559547834719233766229057499219805340125813282416512)
    # print ans