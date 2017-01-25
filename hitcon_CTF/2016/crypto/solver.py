from m1z0r3.crypro import *
from hashlib import sha512

p = 285370232948523998980902649176998223002378361587332218493775786752826166161423082436982297888443231240619463576886971476889906175870272573060319231258784649665194518832695848032181036303102119334432612172767710672560390596241136280678425624046988433310588364872005613290545811367950034187020564546262381876467
remoteip = "133.9.81.203"
remoteport = 1337

def shaint(_str):
    return int(sha512(_str).hexdigest(),16)

def get_pass():
    ans = []
    # Brute Force
    for pos in xrange(11):
        print "Password %s..."%(pos+1)
        for pass_num in xrange(1,17):
            s1,f1 = sock(remoteip,remoteport)
            s2,f2 = sock(remoteip,remoteport)
            s_s1 = []
            s_s2 = []
            for i in xrange(11):
                # Recieve
                read_until(f1,"send ")
                s_s1.append(read_until(f1).strip())

                read_until(f2,"send ")
                s_s2.append(read_until(f2).strip())

                # Exchange
                if i==pos : # Altering the item
                    pass_hash_int = shaint(str(pass_num))
                    send_item = str(pow(pass_hash_int,2,p))
                    s1.send(send_item+"\n")
                    send_item = str(pow(pass_hash_int,2,p))
                    s2.send(send_item+"\n")
                else: # Nomal key exchanging
                    send_item = s_s2[i]
                    s1.send(send_item+"\n")
                    send_item = s_s1[i]
                    s2.send(send_item+"\n")

            read_until(f1,":D): ")
            flag_enc1 = int(read_until(f1))
            read_until(f1)

            read_until(f2,":D): ")
            flag_enc2 = int(read_until(f2))
            read_until(f2)
            s1.close()
            f1.close()
            s2.close()
            f2.close()

            if flag_enc1^int(sha512(s_s1[pos]).hexdigest(),16)==flag_enc2^int(sha512(s_s2[pos]).hexdigest(),16):
                print "Correct!!"
                ans.append(pass_num)
                break
        print ans
        print "-----------------"
    return ans

def last(ans):
    s1,f1 = sock(remoteip,remoteport)
    s_s1 = []
    for i in xrange(11):
        # Recieve
        read_until(f1,"send")
        s_s1.append(read_until(f1).strip())

        # Send
        send_item = str(pow(shaint(str(ans[i])),2,p))
        s1.send(send_item+"\n")
    read_until(f1,":D): ")
    flag_enc1 = int(read_until(f1))
    read_until(f1)
    s1.close()
    f1.close()

    for d in s_s1:
        flag_enc1 ^= int(sha512(d).hexdigest(),16)
    print "[+] flag_int:",flag_enc1
    return hex(flag_enc1)[2:-1].decode("hex")

def main():
    passwords = get_pass()
    print passwords
    flag = last(passwords)
    print flag

if __name__ == '__main__':
    main()