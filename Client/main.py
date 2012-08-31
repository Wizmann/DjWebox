# -*- coding: utf-8 -*-
import httplib,urllib, urllib2
import sys,os
import json
import rsa_pubkey
import binascii
from Crypto.Cipher import AES
from poster.encode import multipart_encode
from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler

try:
    from hashlib import md5
except:
    import md5  

def get_pubkey():
	opener = urllib2.build_opener()
	req = urllib2.Request(
			'http://localhost:8000/handshake'
		)
	r = opener.open(req)
	return open("rsa_server.pub","w").write(r.read())
	
def AES_Decode(key,inputText):
	inputText=binascii.a2b_hex(inputText)
	obj = AES.new(key, AES.MODE_ECB)     
	crypt = obj.decrypt(inputText)
	return crypt.strip()

def register(uname,email,pword):
	uname.strip()
	email.strip()
	pword.strip()
	
	pubkey=get_pubkey()
	_MD5=md5()
	_MD5.update(uname+email+pword)
	pword=_MD5.hexdigest()
	user_data = {
        'uname' : uname,
        'email' : email,
        'pword' : pword,
        }
	json_data=json.dumps(user_data)
	json_data=rsa_pubkey.rsa_encrypt(json_data)
	postdata={'reg_data' : json_data}
	postdata = urllib.urlencode(postdata)
	req = urllib2.Request(
		url = 'http://localhost:8000/register/',
		data = postdata,
		headers = {'User-Agent' : 'Offical Clinet for DjWebox'},
		)
	result = urllib2.urlopen(req).read()
	print result

def login(uname,email,pword):
	uname.strip()
	email.strip()
	pword.strip()
	
	pubkey=get_pubkey()
	_MD5=md5()
	_MD5.update(uname+email+pword)
	pword=_MD5.hexdigest()
	
	user_data = {
        'uname' : uname,
        'email' : email,
        'pword' : pword,
        }
	json_data=json.dumps(user_data)
	json_data=rsa_pubkey.rsa_encrypt(json_data)
	postdata={'login_data' : json_data,'method':'afts'}#Ask for time stamp
	postdata = urllib.urlencode(postdata)
	req = urllib2.Request(
		url = 'http://localhost:8000/login/',
		data = postdata,
		headers = {'User-Agent' : 'Offical Clinet for DjWebox'},
		)
	timeStamp = urllib2.urlopen(req).read()
	timeStamp = AES_Decode(pword,timeStamp)
	print timeStamp
	_MD5=md5()
	_MD5.update(pword+timeStamp)
	pword=_MD5.hexdigest()
	user_data = {
		'uname' : uname,
		'email' : email,
		'pword' : pword,
		}
	json_data=json.dumps(user_data)
	json_data=rsa_pubkey.rsa_encrypt(json_data)
	postdata={'login_data' : json_data,'method':'login'}
	postdata = urllib.urlencode(postdata)
	req = urllib2.Request(
		url = 'http://localhost:8000/login/',
		data = postdata,
		headers = {'User-Agent' : 'Offical Clinet for DjWebox'},
		)
	token=urllib2.urlopen(req).read()
	token=AES_Decode(pword,token)
	return token

def upload(uname,email,pword,token,filepath):
	uname.strip()
	email.strip()
	pword.strip()
	
	filename=filepath.split("\\")[-1]
	_MD5=md5()
	_MD5.update(uname+email+pword)
	auth_code=_MD5.hexdigest()
	_MD5=md5()
	_MD5.update(auth_code+token)
	auth_code=_MD5.hexdigest()
	
	user_data = {
		'uname' : uname,
		'pword' : auth_code,
		'fname' : filename,
		}
	json_data=json.dumps(user_data)
	
	handlers = [StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler]
	opener = urllib2.build_opener(*handlers)
	urllib2.install_opener(opener)
	params = {filepath : open(filepath,'rb')}
	data, headers = multipart_encode(params)
	req = urllib2.Request(
		url = 'http://localhost:8000/upload/',
		data = data,
		headers=headers,
		)
	req.add_header('User-Agent' , 'Offical Clinet for DjWebox')
	req.add_header('Auth-Data' , json_data)
	print urllib2.urlopen(req).read()

def download(uname,email,pword,token,file_request):
	uname.strip()
	email.strip()
	pword.strip()
	_MD5=md5()
	_MD5.update(uname+email+pword)
	auth_code=_MD5.hexdigest()
	_MD5=md5()
	_MD5.update(auth_code+token)
	auth_code=_MD5.hexdigest()
	
	user_data = {
		'uname' : uname,
		'pword' : auth_code,
		'fname' : file_request,
		}
	json_data=json.dumps(user_data)
	postdata={'dwnld_req' : json_data}
	postdata = urllib.urlencode(postdata)
	req = urllib2.Request(
		url = 'http://localhost:8000/download/',
		data = postdata,
		headers = {'User-Agent' : 'Offical Clinet for DjWebox'},
		)
	u = urllib2.urlopen(req)
	f = open(os.path.join(sys.path[0],file_request), 'wb')
	print u.info()
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_request, file_size)

	file_size_dl = 0
	block_sz = 8192
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break

		file_size_dl += len(buffer)
		f.write(buffer)
		status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		status = status + chr(8)*(len(status)+1)
		print status,
	f.close()

def getlist(uname,email,pword,token):
	uname.strip()
	email.strip()
	pword.strip()
	_MD5=md5()
	_MD5.update(uname+email+pword)
	auth_code=_MD5.hexdigest()
	_MD5=md5()
	_MD5.update(auth_code+token)
	auth_code=_MD5.hexdigest()
	
	user_data = {
		'uname' : uname,
		'pword' : auth_code,
		}
	json_data=json.dumps(user_data)
	postdata={'getlist' : json_data}
	postdata = urllib.urlencode(postdata)
	req = urllib2.Request(
		url = 'http://localhost:8000/getlist/',
		data = postdata,
		headers = {'User-Agent' : 'Offical Clinet for DjWebox'},
		)
	return urllib2.urlopen(req).read()

def delete(uname,email,pword,token,file_request):
	uname.strip()
	email.strip()
	pword.strip()
	_MD5=md5()
	_MD5.update(uname+email+pword)
	auth_code=_MD5.hexdigest()
	_MD5=md5()
	_MD5.update(auth_code+token)
	auth_code=_MD5.hexdigest()
	
	user_data = {
		'uname' : uname,
		'pword' : auth_code,
		'fname' : file_request,
		}
	json_data=json.dumps(user_data)
	postdata={'del_req' : json_data}
	postdata = urllib.urlencode(postdata)
	req = urllib2.Request(
		url = 'http://localhost:8000/delete/',
		data = postdata,
		headers = {'User-Agent' : 'Offical Clinet for DjWebox'},
		)
	return urllib2.urlopen(req).read()

if(__name__=='__main__'):
	register('Wizmann','kuuy@foxmail.com','12345678')
	token=login('Wizmann','kuuy@foxmail.com','12345678')
	print getlist("Wizmann",'kuuy@foxmail.com','12345678',token)
	upload("Wizmann",'kuuy@foxmail.com','12345678',token,os.path.join(sys.path[0],'hdu4391.cc'))
	upload("Wizmann",'kuuy@foxmail.com','12345678',token,os.path.join(sys.path[0],'10_Multi.zip'))
	print getlist("Wizmann",'kuuy@foxmail.com','12345678',token)
	download("Wizmann",'kuuy@foxmail.com','12345678',token,'10_Multi.zip')
	print('')
	print delete("Wizmann",'kuuy@foxmail.com','12345678',token,'10_Multi.zip')
	print getlist("Wizmann",'kuuy@foxmail.com','12345678',token)
