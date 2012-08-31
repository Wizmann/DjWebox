#!/usr/bin/env python
# -*- encoding: utf-8 -*- 
import threading
import time
import gobject
import gtk,pygtk 
import sys,os

pygtk.require('2.0') 
gobject.threads_init()


class procDlg():
	def __init__(self,i_status):
		self.gladeFile=sys.path[0]+"/ui.glade"
		self.gladeMain = gtk.Builder() 
		self.gladeMain.add_objects_from_file(self.gladeFile,['procDlg']) 
		self.gladeMain.connect_signals(self)
		
		#添加主界面
		self.mainWindow = self.gladeMain.get_object("procDlg")
		self.mainWindow.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.mainWindow.connect('destroy',lambda q :gtk.main_quit())
		self.mainProBar=self.gladeMain.get_object('p_bar')
		self.timer1 = gobject.timeout_add (100, self.progress_timeout, self.mainProBar)
		self.timer2 = gobject.timeout_add (100, self.is_finished, ()) 
		
		self.status=i_status
		self.mainWindow.show()

	def destroy_progress(self, widget, data=None):  
		gobject.source_remove(self.timer1)
		gobject.source_remove(self.timer2)  
		gtk.main_quit()  
	
	def is_finished(self,*args):
		#print self.status
		if('tag' in self.status and self.status['tag']!=None):
			self.mainProBar.set_text(self.status['tag'])
		else:
			self.mainProBar.set_text(u'请耐心等候')
			
		if(not self.status['running']):
			gobject.source_remove(self.timer1)
			gobject.source_remove(self.timer2) 
			gtk.Widget.destroy(self.mainWindow)
		return True
	
	def progress_timeout(self,pbobj):
		pbobj.pulse()
		pbobj.set_pulse_step(0.01)  
		return True
		
	def main(self):
		gtk.main()
	def gtk_main_quit(self, widget, data=None):
		gtk.main_quit()
