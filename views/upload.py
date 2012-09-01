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
from django.contrib.contenttypes.models import ContentType
from django.db import models

def save_to_box(ifpath,ifname,ibfile):
	try:
		if not isdir(ifpath): # create archive dir if nec.
			makedirs(ifpath)
		of = open(os.path.join(ifpath,ifname), 'wb+')
		if ibfile.multiple_chunks:
			for c in ibfile.chunks():
				of.write(c)
		else:
			of.write(file.read())
		of.close()
	except Exception, e:
		raise Exception(e)

@csrf_exempt
def upload(request):
	try:
		info_dict=json.loads(request.META['HTTP_AUTH_DATA'])
		uname=info_dict['uname']
		auth_code=info_dict['pword']
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
			print auth_code,_MD5.hexdigest()
			if(auth_code==_MD5.hexdigest()):
				for key, bfile in request.FILES.items():
					path = os.path.join(sys.path[0],'FileBox',info_dict['uname'])
					try:
						user=User.objects.get(name=uname)
						try:
							fb=FileBox.objects.get(owner=user,filename=bfile.name)
						except:
							try:
								fb=FileBox(owner=user,filename=bfile.name,position=os.path.join(path,bfile.name))
								fb.save()
							except:
								return HttpResponse("205 Create_FileBox_Error")
							try:
								save_to_box(path,bfile.name,bfile)
							except:
								return HttpResponse("205 Save_to_box_Error")
					except:
						return HttpResponse("999 Unknown User")
					
				return HttpResponse("200 OK")
			else: return HttpResponse("201 Auth Failed!")
	except Exception, e:
		return HttpResponse('999 '+str(e))
