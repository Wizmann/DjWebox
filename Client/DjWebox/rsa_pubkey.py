#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
import base64

import rsa

def rsa_key_export():
	masterkey   = rsa.generate_key( 2048 )
	print '[+] generate OK!'
	print '[+] exporting keypair to disk...'
	rsa.export_keypair( 'rsa_server', masterkey )

	print '\t[+] attempting to reload keypair from disk... ',
	pubkey = rsa.load_key('rsa_server.pub')
	prvkey = rsa.load_key('rsa_server.prv')

	assert( prvkey.has_private() )
	assert( not pubkey.has_private() )
	print 'OK!'
	assert(pubkey == prvkey.publickey())
	
def rsa_encrypt(message,armour = True):
	try:
		key=rsa.load_key('rsa_server.pub')
	except:
		print '[+] load public key error'
		try:
			print '\t[+] attempting to generate new key pair'
			rsa_key_export()
		except:
			print '\t[-] generate new key pair error'
	
	ciphertext  = key.encrypt( message, None )
	ciphertext  = ciphertext[0]

	if armour:
		ciphertext = '\x41' + base64.encodestring( ciphertext )
	else:
		ciphertext = '\x00' + ciphertext

	return ciphertext
	
def rsa_decrypt(message):
	try:
		key=rsa.load_key('rsa_server.prv')
	except:
		print '[+] load public key error'
		try:
			print '\t[+] attempting to generate new key pair'
			rsa_key_export()
		except:
			print '\t[-] generate new key pair error'
		return 'Error'
	if '\x00' == message[0]:
		message = message[1:]
	elif '\x41' == message[0]:
		message = base64.decodestring( message[1:] )

	plaintext   = key.decrypt( message )
	return plaintext
	
def rsa_getPubKey():
	f = open('rsa_server.pub')
	return f.read()
	'''
	except:
		try:
			print '\t[+] attempting to generate new key pair'
			rsa_key_export()
			f = open('rsa_server.pub')
			return f.read()
		except:
			print '\t[-] generate new key pair error'
			return 'Error'
	'''
'''
if(__name__=='__main__'):
	message="你好世界，Hello world."
	t=rsa_encrypt(message)
	print t
	print rsa_decrypt(t)
'''
