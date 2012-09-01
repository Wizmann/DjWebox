#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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
from django.db import models

@csrf_exempt
def download(request):
	if('dwnld_req' in request.POST):
		message=request.POST['dwnld_req']
		info_dict=json.loads(message.strip())
		uname=info_dict['uname']
		auth_code=info_dict['pword']
		fname=info_dict['fname']
		
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
						print fname
						print user
						fb=FileBox.objects.get(filename=fname,owner=user)
						print fb.position
						
						def readFile(fn,buf_size=262144):
							f = open(fn, "rb")
							while True:
								c = f.read(buf_size)
								if c:
									yield c
								else:
									break
							f.close()

						#print readFile(fb.position)
						res=HttpResponse(readFile(fb.position))
						res['Content-Length'] = os.path.getsize(fb.position)
						return res
					except:
						return HttpResponse("No such file!")
				else:
					return HttpResponse("Auth Faild!")
		except Exception,e:
			return HttpResponse(e)
	else:
		return HttpResponse("Bad Request")
