#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import httplib, urllib 
import threading
import time
import gobject
import gtk,pygtk 
import sys,os
import MrCommand as mrc
import globalControl as gctrl
from globalControl import MessageBox
from procDlg import procDlg
from regDlg import regDlg

pygtk.require('2.0')

class loginDlg():
	def __init__(self,res_list):
		self.gladeFile=sys.path[0]+"/ui.glade"
		self.gladeMain = gtk.Builder() 
		self.gladeMain.add_objects_from_file(self.gladeFile,["loginDlg"]) 
		self.gladeMain.connect_signals(self)

		self.mainDlg = self.gladeMain.get_object("loginDlg")
		self.mainDlg.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.mainDlg.connect('destroy',lambda q :gtk.main_quit())
		self.mainDlg.show()
		
		self.gladeMain.get_object("chkbtn_autoLogin").set_active(True)
		gctrl.globalControl.read_from_file()
		self.gladeMain.get_object('entry_name').set_text(gctrl.globalControl.uname)
		self.gladeMain.get_object('entry_email').set_text(gctrl.globalControl.email)
		self.gladeMain.get_object('entry_pword').set_text(gctrl.globalControl.pword)
		self.res_list=res_list
	def main(self):
		gtk.main()
	def gtk_main_quit(self, widget, data=None):
		gtk.main_quit()
		
		
	def on_loginDlg_cancel_clicked(self,*args):
		gtk.Widget.destroy(self.mainDlg)
	
	def on_loginDlg_reg_clicked(self,*args):
		_regdlg=regDlg()
		_regdlg.main()
	
	def on_loginDlg_ok_clicked(self,*args):
		str_name=self.gladeMain.get_object('entry_name').get_text()
		str_email=self.gladeMain.get_object('entry_email').get_text()
		str_pwd=self.gladeMain.get_object('entry_pword').get_text()
		if(str_name=='' or str_email=='' or str_pwd==''):
			gctrl.MessageBox('提示信息','输入有误，请核实','ERROR')
		else:
			class MrLogin(threading.Thread):
				def __init__(self,i_status):
					super(MrLogin, self).__init__()
					self.status=i_status
				def run(self):
					self.status['running']=True
					try:
						self.status['return_value']=mrc.login(str_name,str_email,str_pwd)
					except:
						pass
					self.status['running']=False
			try:
				status={}
				_mrlogin=MrLogin(status)
				_mrlogin.start()
				_procdlg=procDlg(status)
				_procdlg.main()
				return_value=status['return_value']
			except:
				gctrl.MessageBox('提示信息','网络连接错误！','ERROR')
				return 
			try:
				return_value=int(return_value)
				gctrl.MessageBox('提示信息',gctrl.codeToString(return_value),'ERROR')
			except:
				auto_login=self.gladeMain.get_object("chkbtn_autoLogin").get_active()
				if(auto_login):
					gctrl.globalControl.write_to_file()
				######################################
				#TODO:
				#Refresh the file list
				######################################
				gtk.Widget.destroy(self.mainDlg)
				self.res_list.append(True)
