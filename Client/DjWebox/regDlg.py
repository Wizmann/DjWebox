#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import httplib, urllib 
import threading
import time
import gobject
import gtk,pygtk 
import sys,os
import MrCommand as mrc
from globalControl import MessageBox
from procDlg import procDlg
import globalControl as gctrl

pygtk.require('2.0')


class regDlg():
	def __init__(self):
		self.gladeFile=sys.path[0]+"/ui.glade"
		self.gladeMain = gtk.Builder() 
		self.gladeMain.add_objects_from_file(self.gladeFile,["regDlg"]) 
		self.gladeMain.connect_signals(self)

		self.mainDlg = self.gladeMain.get_object("regDlg")
		self.mainDlg.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.mainDlg.connect('destroy',lambda q :gtk.main_quit())
		self.mainDlg.show()
	def main(self):
		gtk.main()
	def gtk_main_quit(self, widget, data=None):
		gtk.main_quit()
		
		
	def on_btn_cancel_clicked(self,*args):
		gtk.Widget.destroy(self.mainDlg)
		
	def on_btn_OK_clicked(self,*args):
		str_name=self.gladeMain.get_object('reg_entry_name').get_text()
		str_email=self.gladeMain.get_object('reg_entry_email').get_text()
		str_pwd1=self.gladeMain.get_object('reg_entry_pword1').get_text()
		str_pwd2=self.gladeMain.get_object('reg_entry_pword2').get_text()
		if(str_name=='' or str_email=='' or str_pwd1!=str_pwd2):
			gctrl.MessageBox('提示信息','输入有误，请核实','ERROR')
		else:
			class MrReg(threading.Thread):
				def __init__(self,i_status):
					super(MrReg, self).__init__()
					self.status=i_status
				def run(self):
					self.status['running']=True
					try:
						self.status['return_value']=mrc.register(str_name,str_email,str_pwd1)
					except:
						pass
					self.status['running']=False
			try:
				status={}
				_mrreg=MrReg(status)
				_mrreg.start()
				_procdlg=procDlg(status)
				_procdlg.main()
				return_value=status['return_value']
			except Exception,e:
				print e
				gctrl.MessageBox('提示信息','网络连接错误！','ERROR')
				return 
			try:
				return_value=int(return_value)
				if(return_value==200):
					gctrl.MessageBox('提示信息','注册成功！','INFO')
					gtk.Widget.destroy(self.mainDlg)
				else:
					gctrl.MessageBox('提示信息',gctrl.codeToString(return_value),'ERROR')
			except Exception,e:
				print e
				gctrl.MessageBox('提示信息','未能解析的错误','INFO')
