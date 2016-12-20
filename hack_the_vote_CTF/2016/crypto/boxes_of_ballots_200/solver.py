from m1z0r3.crypro import *
import json
from Crypto.Cipher import AES
import time

remoteip = "boxesofballots.pwn.republican"
remoteport = 9001

def get_enc(item):
    s,f = sock(remoteip,remoteport)
    j_item = json.dumps(item)
    s.send(j_item+"\n")
    data = read_until(f,"}")
    enc = json.loads(data)["data"]
    return enc

def main():
    item = {"data": "A", "op": "enc"}
    ans = ""
    for i in xrange(1,33):
        print i
        tmp_str = "A"*(32-i)
        item["data"] = tmp_str
        enc1 = get_enc(item)

        for c in readable:
            item["data"] = tmp_str+ans+c
            print tmp_str
            print item["data"]
            print
            enc2 = get_enc(item)
            # print enc2
            if enc1[:64]==enc2[:64]:
                print "OK!"
                ans += c
                print ans
                break
        print "-----------------------------------"
    print "Complete!! The flag is %s"%ans
    s.close()
    f.close()

if __name__ == '__main__':
    main()