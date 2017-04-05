# 0CTF 2017
## oneTimePad2 (Crypto)
ガロア体GF(2^128)上での演算．ガロア体の知識とその演算を行うための環境が必要となる．process1は2数の積，process2は行列の積を取っていることがわかり，nextrand関数で最終的に返される値は (key0 * A^s) + (A^s+1)*B/(A+1) となることがわかる．これを変形してA^sについて式を解き，さらにガロア体上で対数を取ってsを求めることで，nextrandにより得られるkeyを再現することができる．再現して得たkeyのうち最後のキーとciphertxtのxorを取ることでフラグが得られる．
### Require
- SageMath
- PARI/GP
