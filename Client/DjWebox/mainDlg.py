#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import httplib, urllib 
import threading
import time
import gobject
import gtk,pygtk 
import sys,os
import globalControl as gctrl
import MrCommand as mrc
from procDlg import procDlg

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
		self.build_list()
		self.mainDlg.show()
		
		try:
			gctrl.globalControl.read_from_file()
			str_name=gctrl.globalControl.uname
			str_email=gctrl.globalControl.email
			str_pwd=gctrl.globalControl.pword
			class MrLogin(threading.Thread):
				def __init__(self,i_status):
					super(MrLogin, self).__init__()
					self.status=i_status
				def run(self):
					self.status['running']=True
					try:
						self.status['return_value']=mrc.login(str_name,str_email,str_pwd)
					except Exception,e:
						print e
						self.status['return_value']=444
					self.status['running']=False
			try:
				status={}
				_mrlogin=MrLogin(status)
				_mrlogin.start()
				_procdlg=procDlg(status)
				_procdlg.main()
				print status
				return_value=status['return_value']
				try:
					return_value=int(return_value)
					self.gladeMain.get_object("statusbar").push(0, '登录失败：'+gctrl.codeToString(return_value))
				except Exception,e:
					self.gladeMain.get_object("statusbar").push(0, gctrl.globalControl.uname+' 登录成功')
					self.refreshTreeView()
			except Exception,e:
				pass
		except Exception,e:
			print e
			self.gladeMain.get_object("statusbar").push(0, '登录失败：网络连接错误！')
		self.selectedRow=-1
	
	def build_list(self):
		self.mainTreeView=self.gladeMain.get_object('treeview')
		
		column = gtk.TreeViewColumn('文件名', gtk.CellRendererText(),text=0)
		column.set_resizable(True)
		column.set_sort_column_id(0)
		column.set_min_width(250)
		self.mainTreeView.append_column(column)
		
		column = gtk.TreeViewColumn('文件大小(B)', gtk.CellRendererText(),text=1)
		column.set_resizable(True)
		column.set_sort_column_id(1)
		column.set_min_width(250)
		self.mainTreeView.append_column(column)
		
		self.mainList = gtk.ListStore(str,int)
		self.mainTreeView.set_model(self.mainList)
		
	
	def main(self):
		gtk.main()
	def gtk_main_quit(self, widget, data=None):
		gtk.main_quit()
	
	def refreshTreeView(self):
		try:
			self.mainList.clear()
			idict={}
			str_name=gctrl.globalControl.uname
			str_email=gctrl.globalControl.email
			str_pwd=gctrl.globalControl.pword
			res=mrc.getlist(str_name,str_email,str_pwd,idict)
			print res
			if(res!=200 or 'return_value' not in idict):
				self.gladeMain.get_object("statusbar").push(0, '刷新列表失败：'+gctrl.codeToString(res))
			else:
				itemlist=idict['return_value']
				for lines in itemlist.split('\n'):
					print lines
					lines=lines.split('___SPLIT___')
					self.mainList.append([lines[0],int(lines[1])])
		except Exception,e:
			print e
			self.gladeMain.get_object("statusbar").push(0, '刷新列表失败：请先登录或检查网络连接')
		self.selectedRow=-1

	def on_toolbtn_refresh_clicked(self,*args):
		self.refreshTreeView()
	def on_toolbtn_login_clicked(self,*args):
		reslist=[]
		_loginDlg=loginDlg(reslist)
		_loginDlg.main()
		if(len(reslist)!=0 and reslist[0]):
			self.gladeMain.get_object("statusbar").push(0, gctrl.globalControl.uname+' 登录成功')
			self.refreshTreeView()
	def on_toolbtn_upload_clicked(self,*args):
		fcDlg=gtk.FileChooserDialog(title='文件上传',action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		fcDlg.set_default_response(gtk.RESPONSE_OK)
		fcfilter = gtk.FileFilter()
		fcfilter.set_name("All files")
		fcfilter.add_pattern("*")
		fcDlg.add_filter(fcfilter)
		
		response = fcDlg.run()
		if response == gtk.RESPONSE_OK:
			path=fcDlg.get_filename()
			fcDlg.destroy()
			class MrUpload(threading.Thread):
				def __init__(self,i_status):
					super(MrUpload, self).__init__()
					self.status=i_status
				def run(self):
					self.status['running']=True
					str_name=gctrl.globalControl.uname
					str_email=gctrl.globalControl.email
					str_pwd=gctrl.globalControl.pword
					str_token=gctrl.globalControl.token
					try:
						self.status['tag']='正在进行高强度RC4加密...'
						efile=mrc.RC4_Encode_File(str_pwd,path)
						self.status['tag']='正在上传...'
						self.status['return_value']=mrc.upload(str_name,str_email,str_pwd,str_token,efile)
					except Exception,e:
						print 'MrUpload '+str(e)
						self.status['return_value']=205
					finally:
						self.status['running']=False
			status={}
			_mrupload=MrUpload(status)
			_mrupload.start()
			_procdlg=procDlg(status)
			_procdlg.main()
			if('return_value' in status):
				return_value=status['return_value']
				if(return_value==200):
					self.gladeMain.get_object("statusbar").push(0, path.split('/')[-1]+' 上传成功')
				else:
					self.gladeMain.get_object("statusbar").push(0, '上传文件失败：'+gctrl.codeToString(return_value))
			else:
				self.gladeMain.get_object("statusbar").push(0, '上传失败：请先登录或检查网络连接')
		elif response == gtk.RESPONSE_CANCEL:
			fcDlg.destroy()
		
		self.refreshTreeView()
	def on_treeview_cursor_changed(self,*args):
		try:
			self.selectedRow = self.mainTreeView.get_cursor()[0][0]
		except:
			self.selectedRow = -1
	def on_toolbtn_del_clicked(self,*args):
		#print self.mainList.get_value(_iter,0)
		try:
			_iter=self.mainList.get_iter(self.selectedRow)
			value=self.mainList.get_value(_iter,0)
			class MrDel(threading.Thread):
				def __init__(self,i_status):
					super(MrDel, self).__init__()
					self.status=i_status
				def run(self):
					self.status['running']=True
					str_name=gctrl.globalControl.uname
					str_email=gctrl.globalControl.email
					str_pwd=gctrl.globalControl.pword
					str_token=gctrl.globalControl.token
					try:
						self.status['tag']='请求删除数据...'
						self.status['return_value']=mrc.delete(str_name,str_email,str_pwd,str_token,value,self.status)
						if(self.status['return_value']!=200):
							self.status['running']=False
						else:
							pass
					except Exception,e:
						print 'Download '+str(e)
						self.status['return_value']=207
					finally:
						self.status['running']=False
			status={}
			_mrdel=MrDel(status)
			_mrdel.start()
			_procdlg=procDlg(status)
			_procdlg.main()
			return_value=status['return_value']
			print status
			if(return_value!=200):
				self.gladeMain.get_object("statusbar").push(0, '删除失败: '+gctrl.codeToString(return_value))
			else:
				self.gladeMain.get_object("statusbar").push(0, '删除成功: '+value)
				self.refreshTreeView()
		except Exception,e:
			self.gladeMain.get_object("statusbar").push(1, '请选中一个文件')
	def on_toolbtn_download_clicked(self,*args):
		try:
			_iter=self.mainList.get_iter(self.selectedRow)
			value=self.mainList.get_value(_iter,0)
			class MrDownload(threading.Thread):
				def __init__(self,i_status):
					super(MrDownload, self).__init__()
					self.status=i_status
				def run(self):
					self.status['running']=True
					str_name=gctrl.globalControl.uname
					str_email=gctrl.globalControl.email
					str_pwd=gctrl.globalControl.pword
					str_token=gctrl.globalControl.token
					try:
						self.status['tag']='从服务器上下载数据...'
						self.status['return_value']=mrc.download(str_name,str_email,str_pwd,str_token,value,self.status)
						if(self.status['return_value']!=200):
							self.status['running']=False
						else:
							print self.status
							self.status['return_value']=mrc.RC4_Decode_File(str_pwd,self.status['path'])
					except Exception,e:
						print 'Download '+str(e)
						self.status['return_value']=206
					finally:
						self.status['running']=False
			status={}
			_mrdld=MrDownload(status)
			_mrdld.start()
			_procdlg=procDlg(status)
			_procdlg.main()
			return_value=status['return_value']
			print status
			if(return_value!=200):
				self.gladeMain.get_object("statusbar").push(0, '下载失败: '+gctrl.codeToString(return_value))
			else:
				self.gladeMain.get_object("statusbar").push(0, '下载成功: '+status['path'])
		except Exception,e:
			self.gladeMain.get_object("statusbar").push(1, '请选中一个文件')
		
