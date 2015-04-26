from django.db import models
from accounts.models import UserProfile
from Crypto.Cipher import AES
from Crypto import Random
from django.contrib.auth.models import Group
import sys
import time
import pprint 


class Folder(models.Model):
    file_name = models.CharField(max_length=30, default='DEFAULT FOLDER')
    parent_folder = models.ForeignKey("self", related_name='parents', null=True, default=None)
    owner = models.ForeignKey(UserProfile, related_name='folder_set', null=True, default=None)

    def __str__(self):
        return self.file_name


class reports(models.Model):
    author = models.CharField(max_length=30)
    short = models.TextField(max_length=100)
    details = models.TextField()
    location = models.CharField(max_length=100, null=True)
    date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add = True)
    keywords = models.CharField(max_length=100, null=True)
    private = models.BooleanField(default = False)
    encrypt = models.BooleanField(default = False) 
    folder = models.ForeignKey(Folder, related_name='reports_set', null=True, default=None)
    groups = models.ManyToManyField(Group)

    def __str__(self) :
    	return self.short


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    report = models.ForeignKey(reports, null=True)
    md5 = models.CharField(max_length=32, null=True, default="")
    
#    pprint(

'''    def save(self, *args, **kwargs): 
	if not self.id:
		pprint(args, sys.stderr)  			
	super(Document, self).save(*args, **kwargs) '''

class Comment(models.Model):
    name = models.CharField(max_length=42)
    text = models.TextField()
    report = models.ForeignKey(reports)

    def __unicode__(self):
        return self.text