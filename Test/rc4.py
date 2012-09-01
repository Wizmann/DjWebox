#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys,os
import Crypto.Cipher.ARC4 as RC4
import binascii

key='123456789'

def readfile(infile):
	f=open(infile,'rb')
	while True:
		c=f.read(1024)
		if(c):
			yield c
		else:
			break
	f.close()

if(__name__=='__main__'):
	f=open('outfile.bin','wb')
	for pieces in readfile(os.path.join(sys.path[0],'信息安全课程设计题目和要求2012年－3.pdf')):
		f.write(RC4.new(key).encrypt(pieces))
		
	f=open("decodefile.txt","wb")
	for pieces in readfile(os.path.join(sys.path[0],'outfile.bin')):
		f.write(RC4.new(key).decrypt(pieces))
