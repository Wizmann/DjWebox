# -*- coding: utf-8 -*-
import httplib,urllib, urllib2
import sys,os
import json
import rsa_pubkey
import binascii
from Crypto.Cipher import AES
from poster.encode import multipart_encode
from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler
import globalControl as gctrl

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
	crypt = obj.encrypt(padit(inputText))
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
