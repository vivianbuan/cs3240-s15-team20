from django.db import models
import time


class Folder(models.Model):
    file_name = models.CharField(max_length=30, default='DEFAULT FOLDER')

    def __str__(self):
        return self.file_name


class reports(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    short = models.TextField(max_length=100)
    details = models.TextField()
    location = models.CharField(max_length=100, null=True)
    date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add = True)
    keywords = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d', null=True)
    private = models.BooleanField(default = False)
    folder = models.ForeignKey(Folder, default=1)

    def __str__(self) :
    	return self.title

class Document(models.Model):
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')
