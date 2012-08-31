from Crypto.Cipher import AES
import binascii 
try:
    from hashlib import md5
except:
    import md5

def padit(instr):
	add=16-len(instr)%16
	for i in xrange(add):
		instr+=' '
	return instr

_MD5=md5()
_MD5.update('123')
key=_MD5.hexdigest()
obj = AES.new(key, AES.MODE_ECB)     
crypt = obj.encrypt(padit("HELLO"))
print binascii.b2a_hex(crypt)
