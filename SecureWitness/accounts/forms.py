from django import forms
from accounts.models import UserGroup, UserProfile
from django.contrib.auth.models import Group, User
from django.http import Http404

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



class UserGroupCreationForm(forms.Form):
    groupname = forms.CharField(max_length=254)
    username = forms.CharField(max_length=254)

    error_messages = {
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(UserGroupCreationForm, self).__init__(*args, **kwargs)

    def save(self):
        group = Group()
        group.name = self.cleaned_data.get("groupname")
        try:
            userprofile = User.objects.filter(username = self.cleaned_data.get("username"))[0]
        except:
            raise Http404

        u = UserProfile.objects.filter(user=userprofile)

        try:
            u = u[0]
        except:
            raise Http404 ("failed")
        group.save()
        group.user_set.add(userprofile)
        g = UserGroup()
        g.group = group
        g.save()

