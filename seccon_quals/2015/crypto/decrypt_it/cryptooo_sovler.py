from base64 import b64decode
import subprocess
import struct

enc_b64 = "waUqjjDGnYxVyvUOLN8HquEO0J5Dqkh/zr/3KXJCEnw="
enc = b64decode(enc_b64)
print enc
flag = []
charlist = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0","{","}","-","_","+","*","/","?","!",",",".","%","&","=","^","@",":","]","["]
candidate = "SECCON"
output_enc = ""
while len(output_enc) != len(enc):
    for c in charlist:
        cand_tmp = candidate
        cand_tmp += c
        cmd = "./cryptooo %s"%cand_tmp
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print "waiting"
        stdout_data, stderr_data = p.communicate()
        output = stdout_data.split(":")[-1].strip()
        output_enc = b64decode(output)
        if output_enc == enc[:len(output_enc)]:
            break
    candidate = cand_tmp
    print candidate
print candidate