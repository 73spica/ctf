import gmpy
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b

def main():
    n = 98099407767975360290660227117126057014537157468191654426411230468489043009977
    # Used factordb.com
    p = 311155972145869391293781528370734636009
    q = 315274063651866931016337573625089033553

    e = 12405943493775545863
    data = open("./flag.enc").read()
    enc = data.decode("base64")
    i = 0
    while b2l(enc) > n:
        i+=1
        print "Round %s"%i
        print "N is invalid."
        print "calculating p now..."
        p = gmpy.next_prime(p ** 2 + q ** 2)
        print "calculating q now..."
        q = gmpy.next_prime(2 * p * q)
        print "calculating e now..."
        e = gmpy.next_prime(e ** 2)
        print "calculating n now..."
        n = long(p)*long(q)
    print "N is valid!"
    output = "p=%s\nq=%s\nn=%s\ne=%s\n"%(p,q,n,e)
    f = open("param.txt","w")
    f.write(output)
    phi = (p - 1) * (q - 1)
    d = gmpy.invert(e, phi)
    output = "d=%s\nphin=%s"%(d,phi)
    f.write(output)
    f.close()
    dec_int = pow(b2l(enc),d,n)
    decrypted = l2b(dec_int)
    print decrypted

if __name__ == '__main__':
    main()