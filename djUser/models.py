# -*- coding: utf-8 -*-
from django.db import models

class User(models.Model):
	name = models.CharField(max_length=30,unique=True)
	email = models.EmailField(unique=True)
	pword = models.CharField(max_length=60)

	def __unicode__(self):
		return self.name

class Token(models.Model):
	name=models.CharField(max_length=30,unique=True)
	token=models.CharField(max_length=30)
	timeStamp=models.IntegerField()
	
	def __unicode__(self):
		return self.name

class TimeStamp(models.Model):
	name=models.CharField(max_length=30,unique=True)
	timeStamp=models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name

class FileBox(models.Model):
	filename = models.CharField(max_length=64,unique=True)
	owner = models.ForeignKey(User)
	position = models.CharField(max_length=128,unique=True)
	
	def __unicode__(self):
		return self.filename
	
