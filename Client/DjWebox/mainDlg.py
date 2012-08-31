#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import httplib, urllib 
import threading
import time
import gobject
import gtk,pygtk 
import sys,os
import globalControl as gctrl

from loginDlg import loginDlg

pygtk.require('2.0')


class mainDlg():
	def __init__(self):
		self.gladeFile=sys.path[0]+"/ui.glade"
		self.gladeMain = gtk.Builder() 
		self.gladeMain.add_objects_from_file(self.gladeFile,["mainDlg"]) 
		self.gladeMain.connect_signals(self)

		#添加主界面
		self.mainDlg = self.gladeMain.get_object("mainDlg")
		#self.mainDlg.set_default_size(320,240) 
		self.mainDlg.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.mainDlg.connect('destroy',lambda q :gtk.main_quit())
		self.mainDlg.show()
	def main(self):
		gtk.main()
	def gtk_main_quit(self, widget, data=None):
		gtk.main_quit()
	
	def on_toolbtn_login_clicked(self,*args):
		reslist=[]
		_loginDlg=loginDlg(reslist)
		_loginDlg.main()
		if(len(reslist)!=0 and reslist[0]):
			self.gladeMain.get_object("statusbar").push(0, gctrl.globalControl.uname+' 登录成功')
