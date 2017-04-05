int2ff(n, g) = { subst(Pol(digits(n, g.p)), 'x, g) };
ff2int(x) = { subst(x.pol, variable(x.pol), x.p) };

AS = 10921855627060052514492187244493731109
p = 0x100000000000000000000000000000087
print(p)
print(AS)
t = ffgen(2^129)
P = int2ff(p,t).pol
g = ffgen(P*Mod(1,2),'t)
A = 0xc6a5777f4dc639d7d1a50d6521e79bfd
A_poly = int2ff(A,g)
AS_poly = int2ff(AS,g)
print(AS_poly)
print(fflog(AS_poly,A_poly,fforder(A_poly)))

quit
