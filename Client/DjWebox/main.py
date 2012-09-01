#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import httplib, urllib 
import threading
import time
import gobject
import gtk,pygtk 
import sys,os

from mainDlg import mainDlg

pygtk.require('2.0')

if(__name__=='__main__'):
	_mainDlg=mainDlg()
	_mainDlg.main()
