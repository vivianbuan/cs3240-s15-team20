from django.db import models
from accounts.models import UserProfile
# Create your models here.


class Mail(models.Model):
    title = models.TextField(max_length=30, default='No Title')
    details = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True, default=None)
    from_user = models.ForeignKey(UserProfile, related_name='sent_mails', null=True, default=None)
    to_user = models.ForeignKey(UserProfile, related_name='receive_mails', null=True, default=None)

    def __str__(self):
        return self.title + " from " + self.from_user.user.username + " to " + self.to_user.user.username