# -*- coding: utf-8 -*-
import json
import time,random,sys,os
from django import http
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from djUser.models import User,Token,TimeStamp,FileBox
from MrCrypto import rsa_pubkey
try:
	from hashlib import md5
except:
	import md5
from os import makedirs
from os.path import isdir, exists, dirname
from django.contrib.contenttypes.models import ContentType
from django.db import models

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
				return HttpResponse("User Not Found")
			md5_pwd=user.pword
			token_code=token.token;
			timestamp=token.timeStamp;
			now=int(time.time())
			
			if(now-timestamp>=43200):
				#One token is authed for 12 hours
				return HttpResponse("Token Out of Date")
			else:
				_MD5=md5()
				_MD5.update(md5_pwd+token_code)
				if(auth_code==_MD5.hexdigest()):
					try:
						
						#print filelist
						def readlist(fl):
							res=''
							for item in fl:
								res+=str(item.filename)+'\t'+str(round(os.path.getsize(item.position)/1024.,2))+'(kb)'+'\n'	
							return res
						filelist=user.filebox_set.all()
						res=HttpResponse(readlist(filelist))
						return res
					except Exception, e:
						return HttpResponse("Get List Error! "+str(e))
				else:
					return HttpResponse("Auth failed!")
		except Exception,e:
			return HttpResponse(e)
	else:
		return HttpResponse("Bad Request")
						
