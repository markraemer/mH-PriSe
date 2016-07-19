from Crypto.Hash import MD5

pwd = MD5.MD5Hash()
print pwd.new("123456").hexdigest()

hash = MD5.MD5Hash()
print hash.new(pwd.new("AAAAAA").hexdigest()+"inf.hapi@gmail.com").hexdigest()