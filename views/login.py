#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import time,random
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from djUser.models import User,Token,TimeStamp
from MrCrypto import rsa_pubkey
try:
	from hashlib import md5
except:
	import md5
from Crypto.Cipher import AES
import binascii 

def padit(instr):
	add=16-len(instr)%16
	for i in xrange(add):
		instr+=' '
	return instr
    
def random_str(num):
	str_list='abcdefghijklmnoprstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	res=''
	for i in xrange(num):
		res+=random.choice(str_list)
	return res

@csrf_exempt
def login(request):
	if 'login_data' in request.POST and 'method' in request.POST:
		message = request.POST['login_data']
		method = request.POST['method']
		message = rsa_pubkey.rsa_decrypt(message)
		info_dict=json.loads(message.strip())
		#print info_dict
		uname=info_dict['uname']
		pword=info_dict['pword']
		#print uname,pword
		try:
			user=User.objects.get(name=uname)
			if(method == 'afts'):
				print user,"ask for time stamp"
				if(user.pword==pword):
					message='__TIMESTAMP__'+random_str(5)+str(int(time.time()))
					try:
						ts=TimeStamp.objects.get(name=uname)
						ts.timeStamp=message
						ts.save()
						message='200 '+message
					except:
						try:
							ts=TimeStamp(name=uname,timeStamp=message)
							ts.save()
						except:
							message = "333 System Error!"
				else:
					message="201 Password Error!"
			elif(method == 'login'):
				print user,"want login"
				now=int(time.time())
				try:
					ts=TimeStamp.objects.get(name=uname)
					pre=int(ts.timeStamp[len('__TIMESTAMP__')+5:])
					if(now-pre<32):
						_MD5=md5()
						_MD5.update(user.pword+ts.timeStamp)
						if(pword==_MD5.hexdigest()):
							message="__TOKEN__"+random_str(24)
							try:
								tk=Token.objects.get(name=uname)
								tk.token=message
								tk.timeStamp=int(time.time())
								tk.save()
								message='200 '+message
							except:
								try:
									tk=Token(name=uname,token=message,timeStamp=int(time.time()))
									tk.save()
								except:
									message='333 System Error!'
						else:
							message='201 username/password Error'
					else:
						message="202 TimeStamp Overtime!"
						
				except Exception,e:
					print e
					message="202 TimeStamp Error!"
			else:
				message = "999 Unknown Method"
		except Exception, e:
			message='201 '+str(e)
	else:
		message = '333 System Error!'
	try:
		print message
		obj = AES.new(pword, AES.MODE_ECB)     
		crypt = obj.encrypt(padit(message))
		message=binascii.b2a_hex(crypt)
	except:
		message='333 System Error!'
	return HttpResponse(message)
