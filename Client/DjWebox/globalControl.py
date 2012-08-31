# -*- coding: utf-8 -*-

import base64
import os,sys
import gobject
import gtk,pygtk 
import json

from mainDlg import *


def codeToString(x):
	if(x==201): return '认证失败!'
	elif(x==202): return '时间戳失效!'
	elif(x==333): return '系统错误'
	else: return '未知错误'


class globalControl():
	token=''
	uname=''
	email=''
	pword=''
	
	@staticmethod
	def read_from_file():
		try:
			message=base64.decodestring(open(os.path.join(sys.path[0],"info.log")).read().strip())
			info_dict=json.loads(message)
			globalControl.token=info_dict['token']
			globalControl.uname=info_dict['uname']
			globalControl.email=info_dict['email']
			globalControl.pword=info_dict['pword']
		except:
			globalControl.token=globalControl.uname=globalControl.email=globalControl.pword=''
			pass
	
	@staticmethod
	def write_to_file():
		if(globalControl.token!='' and globalControl.uname!='' and globalControl.email!='' and globalControl.pword!=''):
			try:
				info_dict={'token' : globalControl.token,
						   'uname' : globalControl.uname,
						   'email' : globalControl.email,
						   'pword' : globalControl.pword,
						  }
				message=json.dumps(info_dict)
				open(os.path.join(sys.path[0],"info.log"),"w").write(base64.encodestring(message))
			except Exception,e:
				print(e)
		else:
			pass
			
def MessageBox(first_str,second_str,dlgtype):
	type_dict={'INFO' : gtk.MESSAGE_INFO,
			   'WARNING' : gtk.MESSAGE_WARNING,
			   'QUESTION' : gtk.MESSAGE_QUESTION,
			   'ERROR' : gtk.MESSAGE_ERROR,
			  }
	errorMsgBox=gtk.MessageDialog(None,gtk.DIALOG_MODAL,
											type_dict[dlgtype],gtk.BUTTONS_OK,
											first_str)
	errorMsgBox.format_secondary_text(second_str)
	errorMsgBox.run()
	errorMsgBox.destroy()
