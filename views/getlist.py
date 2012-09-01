# -*- coding: utf-8 -*-
import json
import time,random,sys,os
from django import http
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from djUser.models import User,Token,TimeStamp,FileBox
from MrCrypto import rsa_pubkey
import binascii
from Crypto.Cipher import AES
try:
	from hashlib import md5
except:
	import md5
from os import makedirs
from os.path import isdir, exists, dirname
from django.contrib.contenttypes.models import ContentType
from django.db import models

def padIt(inStr):
	add=32-len(inStr)%32
	for i in xrange(add):
		inStr+=' '
	return inStr

def AES_Encode(key,inputText):
	obj = AES.new(key, AES.MODE_ECB)     
	crypt = obj.encrypt(padIt(inputText))
	return binascii.b2a_hex(crypt)


@csrf_exempt
def getlist(request):
	if('getlist' in request.POST):
		message=request.POST['getlist']
		info_dict=json.loads(message.strip())
		uname=info_dict['uname']
		auth_code=info_dict['pword']

		try:
			try:
				user=User.objects.get(name=uname)
				token=Token.objects.get(name=uname)
			except:
				return HttpResponse("201 User_Not_Found")
			md5_pwd=user.pword
			token_code=token.token;
			timestamp=token.timeStamp;
			now=int(time.time())
			
			if(now-timestamp>=43200):
				#One token is authed for 12 hours
				return HttpResponse("201 Token_Out_of_Date")
			else:
				_MD5=md5()
				_MD5.update(md5_pwd+token_code)
				if(auth_code==_MD5.hexdigest()):
					try:
						#print filelist
						def readlist(fl):
							res=''
							for item in fl:
								res+=str(item.filename.encode(sys.getfilesystemencoding()))+'___SPLIT___'+str(os.path.getsize(item.position))+'\n'	
							return res
						filelist=user.filebox_set.all()
						res=HttpResponse('200 '+AES_Encode(user.pword,padIt(readlist(filelist))))
						return res
					except Exception, e:
						print e
						return HttpResponse("333 Get_List_Error! ")
				else:
					return HttpResponse("201 Auth_failed!")
		except Exception,e:
			print str(e)
			return HttpResponse('999 '+str(e))
	else:
		return HttpResponse("204 Bad_Request")
						
