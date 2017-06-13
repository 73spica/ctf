import msgpack
from m1z0r3.crypro import *

def main():
    N = 23927411014020695772934916764953661641310148480977056645255098192491740356525240675906285700516357578929940114553700976167969964364149615226568689224228028461686617293534115788779955597877965044570493457567420874741357186596425753667455266870402154552439899664446413632716747644854897551940777512522044907132864905644212655387223302410896871080751768224091760934209917984213585513510597619708797688705876805464880105797829380326559399723048092175492203894468752718008631464599810632513162129223356467602508095356584405555329096159917957389834381018137378015593755767450675441331998683799788355179363368220408879117131L
    m = open("msg.txt","r").read()
    print "len(m):",len(m)
    m_enc = open("msg.enc", "r").read()
    block1, block2 = msgpack.unpackb(m_enc)
    r_s1, c_s1 = block1
    r_s2, c_s2 = block2
    r1 = int(r_s1.encode("hex"),16)
    c1 = int(c_s1.encode("hex"),16)
    r2 = int(r_s2.encode("hex"),16)
    c2 = int(c_s2.encode("hex"),16)
    #print "r1:",r1
    #print "c1:",c1
    #print "r2:",r2
    #print "c2:",c2
    #print r1-r2
    f_enc = open("flag.enc", "r").read()
    fr_s, fc_s = msgpack.unpackb(f_enc)[0]
    fr = int(fr_s.encode("hex"),16)
    fc = int(fc_s.encode("hex"),16)
    #print "fr:",fr
    #print "fc:",fc
    
    kr1 = c1 * modinv(b2l(m[:256]),N)
    kr2 = c2 * modinv(b2l(m[256:]),N)
    _,a,b = egcd(r1,r2)
    kr2_inv = modinv(kr2,N)
    k = (pow(kr1,a,N) * pow(kr2_inv,-b,N)) % N
    print "k:", k
    print
    print l2b((fc * modinv(pow(k,fr,N),N)) % N )


if __name__ == "__main__":
    main()
