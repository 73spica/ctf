import sys

hash_list = """a : TiKCKWCC
b : HxPCfbCC
c : fJJC+/CC
d : blqCgqCC
e : ghSCMWCC
f : iIzCp/CC
g : MoWCpWCC
h : HozCebCC
i : 0f5CLbCC
j : nigCAWCC
k : AJKCT/CC
l : A8bCMbCC
m : Tx5C0/CC
n : gjbCDqCC
o : nG3CSqCC
p : MtSCnqCC
q : SjSC+qCC
r : +iwC0WCC
s : ijKCDbCC
t : SG5CbWCC
u : eGPCpbCC
v : 0m5CLqCC
w : AinCKqCC
x : biSCgWCC
y : i6PCDWCC
z : +5zCHbCC
A : LxKCTbCC
B : K4gCHWCC
C : fHKCfqCC
D : +GwCbqCC
E : gJSCg/CC
F : M6/Ci/CC
G : phWCM/CC
H : pxWCH/CC
I : eHbC0bCC
J : LjgCnbCC
K : AyGCAqCC
L : TGnCA/CC
M : MgbCTWCC
N : 08KCgbCC
O : DkGCn/CC
P : Sm/CMqCC
Q : nl3CSbCC
R : +tGC+bCC
S : 0xJCibCC
T : DH5CS/CC
U : b4/Ce/CC
V : pfWC0qCC
W : LmnCAbCC
X : KJgCbbCC
Y : g5GCiWCC
Z : D6zC+WCC
0 : fWCCSWCC
1 : HiNCHqCC
2 : HkgCnWCC
3 : n6nCL/CC
4 : LoPCTqCC
5 : TlbCKbCC
6 : KfnCD/CC
7 : DIGCf/CC
8 : fGWCSWCC
9 : S5qCfWCC"""

if len(sys.argv)!=2:
    print "Usage: $ python hash_solver.py [hash_str]"
    sys.exit(0)

hash_list = hash_list.split("\n")
ref_dict = {}
for x in hash_list:
    tmp = x.split(" : ")
    ref_dict[tmp[0]] = tmp[1]
target_hash = sys.argv[1]
block_list = [i+j+k+l for (i,j,k,l) in zip(target_hash[::4],target_hash[1::4],target_hash[2::4],target_hash[3::4])]
print block_list


ans = ""
for block in block_list:
    detect_f = False
    for k,v in ref_dict.items():
        if block.startswith(v[:2]):
            ans += k
            detect_f = True
            break
    if not detect_f:
        pass
        # print block,"block is not detected."
print ans

# def match_test(s1,s2):
#     s1_len = len(s1)
#     s2_len = len(s2)
#     if s1_len<s2_len:
#         print "created hash is longer."
#         criteria_len = s1_len
#     elif s1_len>s2_len:
#         print "created hash is shorter."
#         criteria_len = s2_len
#     else:
#         print "Both hash is same length."
#         criteria_len = s1_len
#     print "s1_len:",s1_len
#     print "s2_len:",s2_len
#     for i in xrange(criteria_len) :
#         if s1[i]==s2[i]:
#             pass
#             # print "same."
#         else:
#             print "defferent!! line %s, s1=%s,s2=%s"%(i,s1[i],s2[i])
#             break