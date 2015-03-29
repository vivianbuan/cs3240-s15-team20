from django.db import models


class Folder(models.Model):
    file_name = models.CharField(max_length=30, default='DEFAULT FOLDER')

    def __str__(self):
        return self.file_name


class reports(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    bodytext = models.TextField()
    timestamp = models.DateTimeField()
    folder = models.ForeignKey(Folder, default=1)

    def __str__(self) :
    	return self.title

