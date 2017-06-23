# coding:utf-8

def I(s):
  val = 0
  for i in range(len(s)):
    digit = ord(s[len(s) - i - 1])
    val <<= 8
    val |= digit
  return val

def Sn(i, length):
  s = ''
  while i != 0:
    digit = i & 0xff
    i >>= 8;
    s += chr(digit)
  return s

def egcd(a, b):
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, p):
  a %= p
  g, x, y = egcd(a, p)
  if g != 1:
    raise Exception('No inverse exists for %d mod %d' % (a, p))
  else:
    return x % p

def add(a, b, p):
  if a == -1:
    return b
  if b == -1:
    return a
  x1, y1 = a
  x2, y2 = b
  x3 = ((x1*x2 - x1*y2 - x2*y1 + 2*y1*y2)*modinv(x1 + x2 - y1 - y2 - 1, p)) % p
  y3 = ((y1*y2)*modinv(x1 + x2 - y1 - y2 - 1, p)) % p
  return (x3, y3)

def double(a, p):
  return add(a, a, p)

def mul(m, g, p):
  r = -1
  while m != 0:
    if m & 1:
      r = add(r, g, p)
    m >>= 1
    g = double(g, p)
  return r

def encrypt(message, key):
  return message ^^ key    

# ==== Baby-step Giant-Step ====
# g^x = A
# let x is m*q-r ( m=cail(sqrt(pi)), q is quotient, r is remainder. )
# g^(m*q-r) = A
# (g^m)^q = A*g^r
# Compute the right side and the left side respectively.
def bsgs(g, y, pk, order):
    m = int(sqrt(pk))
    print "m:",m
    gm = mul(m,g,pk)
    g_r_dict = {}
    g_r = g
    print "Baby-step"
    for r in xrange(1,m):
        g_r_dict[(add(y,g_r,pk))] = r 
        g_r = add(g_r,g,pk) # g^-2=g^-1 + g^-1, g^-3=g^-2 + g^-1

    gmq = gm
    print "Giant-step"
    for q in xrange(1,m):
        if gmq in g_r_dict:
            print "Congrats!"
            return m*q - g_r_dict[gmq] % pk
        gmq = add(gmq,gm,pk)
    return None
        
#==== Chinese remainder theorem ====
def crt(crtlist):
    def mod_product(crtlist):
        ans = 1
        for _,mod in crtlist:
            ans *= mod
        return ans
    def crt_sum(anslist,M):
        ans = 0
        for x in anslist:
            ans = (ans+x) % M
        return ans
    M = mod_product(crtlist)
    anslist = []
    for a,mod in crtlist:
        x = M/mod # M/mi
        y = modinv(x,mod)
        anslist.append(x*y*a)
    return crt_sum(anslist,M)
    
def calc_order(plist):
    ans = 1
    for d in plist:
        ans *= d-1
    return ans

def main():
    enc_msg = 137737300119926924583874978524079282469973134128061924568175107915062758827931077214500356470551826348226759580545095568667325
    flag_len = 31

    # Modulus
    p = 606341371901192354470259703076328716992246317693812238045286463
    # g is the generator point.
    g = (160057538006753370699321703048317480466874572114764155861735009, 255466303302648575056527135374882065819706963269525464635673824)
    # Alice's public key A:
    A = (460868776123995205521652669050817772789692922946697572502806062, 263320455545743566732526866838203345604600592515673506653173727)
    # Bob's public key B:
    B = (270400597838364567126384881699673470955074338456296574231734133, 526337866156590745463188427547342121612334530789375115287956485)

    print "==== Calculating Order ===="
    p_fact = str(factor(p))
    #p_fact = "901236131 * 911236121 * 921236161 * 931235651 * 941236273 * 951236179 * 961236149"
    print "factor(p):", p_fact

    plist = map(int,p_fact.split(" * "))
    order = calc_order(plist)
    print "order:",order
    

    Bak_list = []
    i=0
    print "==== Baby-Step Giant-Step ===="
    for pk in plist:
        ak = bsgs(g, A, pk, order)
        if ak == None:
            return
        i+=1
        print "a%s = %s"%(i,ak)
        Bak_list.append(mul(ak,B,pk))
        print "------------"
    #Bak_list = [(437446849, 262102750), (449495890, 520618997), (361115209, 589220969), (902699770, 291559125), (118786135, 8052119), (843063656, 156615361), (935664187, 688700344)]
    print "B^ak List:",Bak_list
    print

    print "==== Chinese remainder theorem ===="
    crt_listx = []
    crt_listy = []
    for i in xrange(len(plist)):
        crt_listx.append([Bak_list[i][0],plist[i]])
        crt_listy.append([Bak_list[i][1],plist[i]])
    bothMS = []
    bothMS.append(crt(crt_listx))
    bothMS.append(crt(crt_listy))
    print "bothMS:",bothMS
    print

    masterSecret = bothMS[0] * bothMS[1]
    flag = encrypt(enc_msg,masterSecret)
    print Sn(flag,31)

if __name__ == "__main__":
    main()
