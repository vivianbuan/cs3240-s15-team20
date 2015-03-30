from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username


class UserGroup(models.Model):
    group = models.OneToOneField(Group)

    def __str__(self):
        return self.group.name

