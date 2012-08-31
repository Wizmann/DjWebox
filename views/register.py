# -*- coding: utf-8 -*-
from django.http import HttpResponse
from djUser.models import User
from MrCrypto import rsa_pubkey
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
	if 'reg_data' in request.POST:
		message = request.POST['reg_data']
		message = rsa_pubkey.rsa_decrypt(message)

		info_dict=json.loads(message.strip())
		print info_dict
		new_user=User(name=info_dict['uname'],
					  email=info_dict['email'],
					  pword=info_dict['pword'],
					 )
		try:
			new_user.save()
			message='200 OK'
		except Exception,e:
			print e
			message='203 DataBase Error'
	else:
		message = '204 Bad Request'
	return HttpResponse(message)
