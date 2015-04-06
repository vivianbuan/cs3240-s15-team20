from django import forms
from accounts.models import UserGroup
from django.contrib.auth.models import Group

class GroupCreationForm(forms.Form):
    groupname = forms.CharField(max_length=254)

    error_messages = {
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(GroupCreationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        
    def save(self):
        group = Group()
        group.name = self.cleaned_data.get("groupname")
        group.save()
        g = UserGroup()
        g.group = group
        g.save()

