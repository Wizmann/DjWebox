#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import httplib,urllib, urllib2
import sys,os
import json
import rsa_pubkey
import binascii
from Crypto.Cipher import AES
import Crypto.Cipher.ARC4 as RC4
from poster.encode import multipart_encode
from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler
import globalControl as gctrl
import glib
import time

try:
    from hashlib import md5
except:
    import md5  

def padIt(inStr):
	add=32-len(inStr)%32
	for i in xrange(add):
		inStr+=' '
	return inStr

def get_pubkey():
	opener = urllib2.build_opener()
	req = urllib2.Request(
			'http://localhost:8000/handshake'
		)
	r = opener.open(req)
	return open("rsa_server.pub","w").write(r.read())


def AES_Encode(key,inputText):
	obj = AES.new(key, AES.MODE_ECB)     
	crypt = obj.encrypt(padIt(inputText))
	return binascii.b2a_hex(crypt)

def AES_Decode(key,inputText):
	inputText=binascii.a2b_hex(inputText)
	obj = AES.new(key, AES.MODE_ECB)     
	crypt = obj.decrypt(inputText)
	return crypt.strip()

def MD5_Encode(instr):
	_MD5=md5()
	_MD5.update(instr)
	return _MD5.hexdigest()

def _readfile(infile,buf_siz=65535):
	f=open(infile,'rb')
	while True:
		c=f.read(buf_siz)
		if(c):
			yield c
		else:
			break
	f.close()

def RC4_Encode_File(key,path):
	filename=path.split('/')[-1]
	encode_path=os.path.join('/tmp',filename)
	f=open(encode_path,'wb')
	for pieces in _readfile(path):
		f.write(RC4.new(key).encrypt(pieces))
	return encode_path

def RC4_Decode_File(key,path):
	filename=path.split('/')[-1]
	decode_path=os.path.join('/tmp',filename)
	f=open(path,'wb')
	for pieces in _readfile(decode_path):
		f.write(RC4.new(key).decrypt(pieces))
	return 200
	
	
def login(uname,email,pword):
	uname=uname.strip()
	email=email.strip()
	pword=pword.strip()
	oripword=pword
	pubkey=get_pubkey()
	pword=MD5_Encode(uname+email+pword)
	
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
	try:
		#print timeStamp
		timeStamp=timeStamp.split()
		code=int(timeStamp[0])
		if(code==200):
			timeStamp=timeStamp[1].strip()
		else:
			return code
	except:
		return 999
	#We got the time stamp for login now
	
	pword=MD5_Encode(pword+timeStamp)
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
	try:
		print token
		token=token.split()
		code=int(token[0])
		if(code==200):
			token=token[1].strip()
			gctrl.globalControl.uname=uname
			gctrl.globalControl.email=email
			gctrl.globalControl.pword=oripword
			gctrl.globalControl.token=token
		else:
			return code
	except:
		return 999
		
def register(uname,email,pword):
	uname=uname.strip()
	email=email.strip()
	pword=pword.strip()
	
	pubkey=get_pubkey()
	pword=MD5_Encode(uname+email+pword)
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
	return result.split()[0]

def getlist(uname,email,pword,idic):
	uname=uname.strip()
	email=email.strip()
	pword=pword.strip()
	
	pword=MD5_Encode(uname+email+pword)
	auth_code=MD5_Encode(pword+gctrl.globalControl.token)
	
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
	res=urllib2.urlopen(req).read().split()
	print res
	try:
		if(int(res[0])==200):
			res[1]=AES_Decode(pword,res[1])
			idic['return_value']=res[1]
			return 200
		else:
			return int(res[0])
	except Exception,e:
		print e
		return 999
		
def upload(uname,email,pword,token,filepath):
	uname=uname.strip()
	email=email.strip()
	pword=pword.strip()
	
	filename=filepath.split("/")[-1].strip()
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
	filepath = filepath.decode(sys.getfilesystemencoding())
	params = {filepath : open(filepath,'rb')}
	data, headers = multipart_encode(params)
	req = urllib2.Request(
		url = 'http://localhost:8000/upload/',
		data = data,
		headers=headers,
		)
	req.add_header('User-Agent' , 'Offical Clinet for DjWebox')
	req.add_header('Auth-Data' , json_data)
	res=urllib2.urlopen(req).read()
	return int(res.split()[0])
	
def download(uname,email,pword,token,file_request,i_status):
	try:
		uname=uname.strip()
		email=email.strip()
		pword=pword.strip()
		file_request=file_request.strip()

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
		downloads_dir = glib.get_user_special_dir(glib.USER_DIRECTORY_DOWNLOAD)
		f = open(os.path.join('/tmp',file_request), 'wb')
		print u.info()
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (file_request, file_size)
		i_status['tag']='文件大小 %s kb' % (str(round(file_size / 1024.,2)))
		time.sleep(1)
		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break

			file_size_dl += len(buffer)
			f.write(buffer)
			i_status['tag']='已下载 : %.2f%%' % (file_size_dl * 100. / file_size)
			if(i_status['running']==False):
				raise 'Abort'
				break
		f.close()
		i_status['path']=os.path.join(downloads_dir,file_request)
		return 200
	except Exception,e:
		print e
		return 206

def delete(uname,email,pword,token,file_request,i_status):
	uname=uname.strip()
	email=email.strip()
	pword=pword.strip()
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
	res=urllib2.urlopen(req).read()
	return int(res.split()[0])
