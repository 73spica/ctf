require 'openssl'
require 'webrick'
require 'base64'
require 'json'
require 'zlib'
# require 'pry'
def encrypt(data)
  cipher = OpenSSL::Cipher::AES.new(128, :CTR)
  cipher.encrypt
  key = cipher.random_key
  print key.size ,"\n"
  iv = cipher.random_iv
  print iv.length,"\n"
  cipher.auth_data = ""
  encrypted = cipher.update(data) + cipher.final
  return encrypted
end

def get_auth(user)
  user = 'flag"flag'
  data = [user, "flag:nanamichiaki_is_very_cute."]
  json = JSON.dump(data)
  print json+"\n"
  zip = Zlib.deflate(json)
  print zip+"\n"
  return Base64.strict_encode64(encrypt(zip))
end

print get_auth("hoge")

