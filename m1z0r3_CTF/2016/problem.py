#!/usr/bin/env python
# coding: utf-8

import os,cgi,Cookie
from Crypto.Cipher import AES
from base64 import b64encode,b64decode

key = u"xxxxxxxxxxxxxxxx"
iv = u"xxxxxxxxxxxxxxxx"

def is_ascii(_str):
    return max([ord(c) for c in _str]) < 128

def decode_hex(_str):
    if len(_str)%2!=0:
        _str = "0"+_str
    return _str.decode("hex")


html_body = u"""
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8"> </head>
<body>
  <div style="text-align:center;margin-top:50px;">
  <form action="/cgi-bin/problem.py" method="POST">
    Input Ciphertext:
    <input type="text" name="cipher" size=40/>
    <button type="submit" name="decrypt">Decrypt</button>
  </form>
  <div id="result">%s</div>
  </div>
</body>
</html>"""

content=''
sc = Cookie.SimpleCookie(os.environ.get('HTTP_COOKIE',''))
if sc.get('iv') is None:
    sc['iv'] = b64encode(iv)
    print sc.output()

form=cgi.FieldStorage()
hex_cipher=form.getvalue('cipher', '')

if len(hex_cipher)!=32:
    pass
    #content=u"16byteの暗号文の16進数を入力してください"
else:
    # ==== Decryption ====
    ## One round for now. I'll write it later...
    cipher = hex_cipher.decode("hex")
    aes = AES.new(key,AES.MODE_ECB)
    dec = aes.decrypt(cipher)
    dec = int(dec.encode("hex"),16)^int(b64decode(sc.get('iv').value).encode("hex"),16)
    content = decode_hex(hex(dec)[2:-1])
    if not is_ascii(content):
        content = "The result of decryption contains non-ASCII characters. Something wrong."

print "Content-type: text/html;charset=utf-8\n"
print (html_body % content).encode('utf-8')