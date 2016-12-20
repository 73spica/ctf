import requests
import binascii
import sys
from base64 import b64decode
import string
from m1z0r3.crypro import *
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

def brute(key):
    tmplen = 0
    for c in alpha:
        senddata = (key + c) * 10
        url = 'https://cthulhu.fluxfingers.net:1505/?user=%s'%senddata
        r = requests.get(url,verify=False)
        deflate =  b64decode(r.cookies['auth'])
        l = len(deflate)
        # print "[+] senddata = " + senddata
        # print "[+] len  = " + str(l)
        if tmplen>l:
            return key+c
        tmplen = l
    return key+alpha[0]

alpha = readable

def main():
    nowans = 'flag:'
    while nowans!= 0:
      nowans = brute(nowans)
      print nowans
      if nowans[-1]=='"':
        break
    print "Complete!! The answer is %s"%nowans[:-1]

if __name__ == '__main__':
    main()
