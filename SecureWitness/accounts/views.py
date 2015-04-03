from django.shortcuts import render, HttpResponseRedirect

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.db.models import Q
from accounts.models import UserProfile
from Report.models import Folder
from Report.models import reports

# Create your views here.

@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request, creation_form=UserCreationForm,extra_context=None):

    if request.method == "POST":
        # Add User Model instance here
        form = creation_form(data=request.POST)
        if form.is_valid() :
            user = form.save()
            profile = UserProfile(user = user)
            profile.save()
            user = authenticate(username=form.cleaned_data.get("username"),
                         password=form.cleaned_data.get("password1"))
            login(request,user)
            return HttpResponseRedirect("/")
    else :
        form = creation_form(request)

    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, "registration/register.html", context)


def profile(request):
    folders = Folder.objects.all()[:20]
    return render(request, 'user_profile.html', {'folder': folders})


def report_list(request, folder_id):
    return render(request, 'report_list.html', {'folder': Folder.objects.all().filter(pk=folder_id)[0]})

