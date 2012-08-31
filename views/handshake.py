# -*- coding: utf-8 -*-
from django.http import HttpResponse
from MrCrypto import rsa_pubkey

def handshake(request):
	return HttpResponse(rsa_pubkey.rsa_getPubKey())
