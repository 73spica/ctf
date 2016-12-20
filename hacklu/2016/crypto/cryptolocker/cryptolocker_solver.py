import sys
import hashlib
from AESCipher import *
from itertools import product
from m1z0r3.crypro import *

# We need to move to cryptolocker directory.

class SecureEncryption(object):
    def __init__(self, keys):
        assert len(keys) == 4
        self.keys = keys
        self.ciphers = []
        for i in range(4):
            self.ciphers.append(AESCipher(keys[i]))

    def dec(self, ciphertext):
        three      = AESCipher._unpad(self.ciphers[3].decrypt(ciphertext))
        two        = AESCipher._unpad(self.ciphers[2].decrypt(three))
        one        = AESCipher._unpad(self.ciphers[1].decrypt(two))
        plaintext  = AESCipher._unpad(self.ciphers[0].decrypt(one))
        return plaintext

    # self-made
    def step_dec(self, ciphertext, k):
        if k==3:
            three = self.ciphers[3].decrypt(ciphertext)
            return three

        three = AESCipher._unpad(self.ciphers[3].decrypt(ciphertext))

        if k==2:
            two = self.ciphers[2].decrypt(three)
            return two

        two = AESCipher._unpad(self.ciphers[2].decrypt(three))
        
        if k==1:
            one = self.ciphers[1].decrypt(two)
            return one
        one = AESCipher._unpad(self.ciphers[1].decrypt(two))

        if k==0:
            plaintext = self.ciphers[0].decrypt(one)
        return plaintext

def check_pad(_str):
    pad = _str[-2:]
    if pad=="01":
        return False
    padlen = int(pad,16)
    padp = padlen*2
    if _str[-padp:]==pad*padlen:
        print "  "+_str
        return True
    else:
        return False

if __name__ == "__main__":
    chars = readable
    key_num = 3
    true_keys = ["aa","aa","aa","aa"]
    keys = [ # Four times 256 is 1024 Bit strength!! Unbreakable!!
            hashlib.sha256(true_keys[0]).digest(),
            hashlib.sha256(true_keys[1]).digest(),
            hashlib.sha256(true_keys[2]).digest(),
            hashlib.sha256(true_keys[3]).digest(),
    ]
    f = open("flag.encrypted","rb")
    ciphertext = f.read()
    f.close()
    for key_num in reversed(xrange(4)):
        print " Detecting key%s..."%key_num
        for x in product(chars, repeat=2):
            x = "".join(x)

            keys[key_num] = hashlib.sha256(x).digest()####
            s = SecureEncryption(keys)
            plaintext_ = s.step_dec(ciphertext,key_num)

            if check_pad(plaintext_.encode("hex")[-64:]):
                true_keys[key_num] = x
                print "  - key3 is",true_keys[3] ####
                print "  - key2 is",true_keys[2] ####
                print "  - key1 is",true_keys[1] ####
                print "  - key0 is",true_keys[0] ####
                print "---------------------------"
                break

    s = SecureEncryption(keys)
    plaintext_ = s.dec(ciphertext)
    f_write = open("test_ans.odt","w")
    f_write.write(plaintext_)
    f_write.close()
    print "Complete."