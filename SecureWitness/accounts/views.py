from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.db.models import Q
from accounts.models import UserProfile, UserGroup
from Report.models import Folder
from Report.models import reports
from accounts.forms import GroupCreationForm, UserGroupCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.

@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request, creation_form=UserCreationForm, extra_context=None):

    if request.method == "POST":
        # Add User Model instance here
        form = creation_form(data=request.POST)
        if form.is_valid() :
            user = form.save()
            profile = UserProfile(user = user)
            profile.save()
            user = authenticate(username=form.cleaned_data.get("username"),
                         password=form.cleaned_data.get("password1"))
            login(request, user)
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
    if len(folders) == 0:
        folder = Folder()
        folder.save()
        # folders = Folder.objects.all()[:20]
    # This code allows for an admin link on the user profile page.
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None

    root_folder = Folder.objects.get(pk=1)
    return render(request, 'user_profile.html', {'o': root_folder, 'prof': profile})


def report_list(request, folder_id):
    return render(request, 'report_list.html', {'folder': Folder.objects.filter(pk=folder_id)[0]})


def add_folder(request):
    if request.method == 'POST':
        title = request.POST.get("file_name")

        # handel invalid input
        if len(title) == 0:
            error = "Error: folder name needed!"
            folders = Folder.objects.all()[:20]
            return render(request, 'add_folder.html', {'folder': folders, 'message': error})
        elif Folder.objects.filter(file_name=title).count() != 0:
            error = "Error: folder already exist!"
            folders = Folder.objects.all()[:20]
            return render(request, 'add_folder.html', {'folder': folders, 'message': error})
        else:
            parent_name = request.POST.get("parent_folder")
            parent = Folder.objects.get(file_name=parent_name)
            folder = Folder(file_name=title, parent_folder=parent)
            folder.save()

        if request.user.is_active:
            profile = UserProfile.objects.filter(user = request.user)[0]
        else:
            profile = None

        root_folder = Folder.objects.get(pk=1)
        return render(request, 'user_profile.html', {'o': root_folder, 'prof': profile})

    folders = Folder.objects.all()[:20]
    error = ""
    return render(request, 'add_folder.html', {'folder': folders, 'message': error})


def edit_folder(request, folder_id):
    if request.method == 'POST':
        # handle different request
        if request.POST.get("cancel"):     # Cancel
            return render(request, 'report_list.html', {'folder': Folder.objects.filter(pk=folder_id)[0]})
        elif request.POST.get("save"):     # Save changes
            current_folder = Folder.objects.filter(pk=folder_id)[0]
            title = request.POST.get("file_name")
            parent_name = request.POST.get("parent_folder")
            parent = Folder.objects.get(file_name=parent_name)
            if parent.parent_folder == current_folder:
                    error = "Error: Your target folder " + parent_name + "is  currently in " + current_folder.file_name
                    folders = Folder.objects.all()[:20]
                    return render(request, 'edit_folder.html', {'current': current_folder, 'folder': folders, 'message': error})
            elif len(title) == 0:
                    current_folder.parent_folder = parent
                    current_folder.save()
                    return render(request, 'report_list.html', {'folder': current_folder})
            elif parent.parents.filter(file_name=title).count() != 0:
                error = "Error: Folder " + title + " already exist in the target folder " + parent_name
                folders = Folder.objects.all()[:20]
                return render(request, 'edit_folder.html', {'current': current_folder, 'folder': folders, 'message': error})
            else:
                    current_folder.file_name = title
                    current_folder.parent_folder = parent
                    current_folder.save()
                    return render(request, 'report_list.html', {'folder': current_folder})
        elif request.POST.get("delete"):   # Delete folder
            get_object_or_404(Folder, pk=folder_id).delete()
            root_folder = Folder.objects.get(pk=1)
            if request.user.is_active:
                profile = UserProfile.objects.filter(user = request.user)[0]
            else:
                profile = None
            return render(request, 'user_profile.html', {'o': root_folder, 'prof': profile})
        else:                               # only for debug issue
            error = "Error: button not working!"
            current_folder = Folder.objects.filter(pk=folder_id)[0]
            folders = Folder.objects.all()[:20]
            return render(request, 'edit_folder.html', {'current': current_folder, 'folder': folders, 'message': error})

    current_folder = Folder.objects.filter(pk=folder_id)[0]
    folders = Folder.objects.all()[:20]
    error = ""
    return render(request, 'edit_folder.html', {'current': current_folder, 'folder': folders, 'message': error})


def admin_page(request):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    Groups = UserGroup.objects.all()[:20]
    Users = UserProfile.objects.all()[:20]

    context = {'groups' : Groups, 'users' : Users}
    return render(request, 'admin/main.html', context)


def admin_user(request, user_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    context = {'u' : UserProfile.objects.filter(pk=user_id)[0]}
    return render(request, 'admin/user.html', context)


def admin_group(request, group_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    return render(request, 'admin/group.html')

@sensitive_post_parameters()
@csrf_protect
@never_cache
def admin_creategroup(request, creation_form=GroupCreationForm):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    if request.method == "POST":
        form = creation_form(data=request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect("/accounts/admin")
    else :
        form = creation_form(request)

    context = {
        'form': form,
    }
    return render(request, "admin/creategroup.html", context)


def admin_deleteuser(request, user_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    u = UserProfile.objects.filter(pk=user_id)[0]
    u_u = u.user
    u.delete()
    u_u.delete()
    return render(request, 'admin/action_complete.html')


def admin_makeadmin(request, user_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    u = UserProfile.objects.filter(pk=user_id)[0]
    u.administrator = 1
    u.save()
    return render(request, 'admin/action_complete.html')


def admin_group_adduser(request):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

def check_user_fail(request):
    try:
        profile = UserProfile.objects.filter(user = request.user)[0]
    except IndexError:
        return True
    if not profile.is_admin :
        return True


@login_required(login_url="/accounts/login/")
def add_group(request, creation_form=UserGroupCreationForm):
    if request.method == "POST":
        form = creation_form(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form=creation_form(request)
    context = {
        'form' : form,
    }
    return render(request, "add_group.html")
