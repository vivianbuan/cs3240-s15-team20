from django.db import models


class reports(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    bodytext = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self) :
    	return self.title

