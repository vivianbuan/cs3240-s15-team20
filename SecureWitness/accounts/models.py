from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username

    administrator = models.BooleanField(default=0)

    @property    
    def is_admin(self):
        return bool(self.administrator)

    def make_admin(self,admin):
        self.administrator = admin

    @property    
    def date_joined(self):
        return self.user.date_joined


class UserGroup(models.Model):
    group = models.OneToOneField(Group)

    def __str__(self):
        return self.group.name
