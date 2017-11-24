# coding:utf-8
#!/usr/bin/python2

from flag import flag
from SocketServer import ThreadingTCPServer
from sys import exit
import SocketServer
from Crypto.Util.number import *
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b
from random import randint

MAX_TRIES = 1024

welcome = "Welcome to My Crypto System!!\n"
menu = "What would you like to do:\n\t[1]: Encryption,\n\t[2]: Decryption,\n\t[3]: Get flag cipher,\n\t[4]: Get public key,\n\t[5]: Exit.\n> "

# ======== Extended Euclidean algorithm ========
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# ======== mod inverse ========
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

class MyCrypto:
    class Pubkey:
        def __init__(self):
            pass
        def setKey(self, y, g, p):
            self.y = y
            self.g = g
            self.p = p
        def show(self):
            print "y:",self.y
            print "g:",self.g
            print "p:",self.p
    def __init__(self):
        self.pubkey = self.Pubkey()

    def genKey(self, bits):
        p = getPrime(bits)
        g = randint(1,p-1)
        x = randint(1,p-1)
        y = pow(g,x,p)
        self.seckey = x
        self.pubkey.setKey(y, g, p)

    def enc(self, plain):
        y = self.pubkey.y
        g = self.pubkey.g
        p = self.pubkey.p

        m = b2l(plain)
        r = randint(1,p-1)
        c1 = pow(g, r, p)
        c2 = ( pow(y, r, p) * m ) % p
        cipher = (c1, c2)
        return cipher

    def dec(self, cipher):
        c1, c2 = cipher
        p = self.pubkey.p
        x = self.seckey
        
        m = (pow(modinv(c1,p),x,p) * c2) % p
        return m

class B64Handler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.tries = 0
        self.crypto = MyCrypto()
        self.crypto.genKey(512)
        self.enc_flag = self.crypto.enc(flag)
        #self.crypto.pubkey.show()
        #print self.crypto.seckey

    def handle(self):
        self.request.send(welcome)
        for i in range(MAX_TRIES):
            self.request.send(menu)
            cmd = self.request.recv(2)[0]
            if cmd == "1":
                self.request.send("You selected 1.\n")
                self.request.send("Please input your message: ")
                msg = self.request.recv(4096).strip()
                self.request.send(str(self.crypto.enc(msg)))
            elif cmd == "2":
                self.request.send("You selected 2.\n")
                self.request.send("Please input your cipher.\n")
                self.request.send("c1: ")
                c1 = self.request.recv(4096).strip()
                self.request.send("c2: ")
                c2 = self.request.recv(4096).strip()
                try:
                    c = (long(c1),long(c2))
                except:
                    self.request.send("Error: You must send a number as c1 and c2.")
                    exit(0)
                self.request.send(str(self.crypto.dec(c) & 1))
            elif cmd == "3":
                self.request.send("You selected 3.\n")
                self.request.send("The flag Cipher: {}\n".format(self.enc_flag))
            elif cmd == "4":
                self.request.send("You selected 4.\n")
                self.request.send("(y, g, p): {}\n".format((self.crypto.pubkey.y, self.crypto.pubkey.g, self.crypto.pubkey.p)))
            else:
                self.request.send("Bye.\n")
                exit(0)
            self.request.send("\n-------------------------\n")

        self.request.send("Bye.\n")

def main():
    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    LOCAL_PORT = 12345
    s = SocketServer.ThreadingTCPServer(("", LOCAL_PORT), B64Handler)
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        print("shutting down")
        s.shutdown()
        s.socket.close()

if __name__ == "__main__":
    main()

