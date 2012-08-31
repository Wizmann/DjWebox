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
from django.db import models

@csrf_exempt
def delete(request):
	if('del_req' in request.POST):
		message=request.POST['del_req']
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
						fb=FileBox.objects.get(filename=fname,owner=user)
						os.remove(fb.position)
						fb.delete()
						return HttpResponse("OK")
					except:
						return HttpResponse("No such file!")
				else:
					return HttpResponse("Auth Faild!")
		except Exception,e:
			return HttpResponse(e)
	else:
		return HttpResponse("Bad Request")
