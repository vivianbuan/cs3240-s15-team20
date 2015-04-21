from django.conf import settings

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, resolve_url

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.db.models import Q
from accounts.models import UserProfile, UserGroup
from Report.models import Folder
from Report.models import reports
from accounts.forms import GroupCreationForm, UserGroupCreationForm, GroupAdditionForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
                                 logout as auth_logout, get_user_model, update_session_auth_hash)

from django.template.response import TemplateResponse
from django.utils.http import is_safe_url

# Create your views here.

@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request, creation_form=UserCreationForm, extra_context=None):
    form = creation_form(request.POST or None)
    if request.method == "POST":
        # Add User Model instance here
        if form.is_valid():
            user = form.save()
            profile = UserProfile(user=user)
            profile.save()
            user = authenticate(username=form.cleaned_data.get("username"),
                                password=form.cleaned_data.get("password1"))
            login(request, user)
            return HttpResponseRedirect("/")
    context = {
    'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, "registration/register.html", context)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        if request.POST.get("login"):
            form = authentication_form(request, data=request.POST)
            if form.is_valid():
                # Ensure the user-originating redirection url is safe.
                if not is_safe_url(url=redirect_to, host=request.get_host()):
                    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

                # Okay, security check complete. Log the user in.
                profile = UserProfile.objects.filter(user=form.get_user())
                if len(profile) is 0:
                    context = {
                        'form': form,
                        redirect_field_name: redirect_to,
                    }
                    if extra_context is not None:
                        context.update(extra_context)
                    return TemplateResponse(request, template_name, context,
                                        current_app=current_app)

                profile = profile[0]
                if profile.is_suspended:
                    return render(request, 'registration/suspended.html')

                auth_login(request, form.get_user())

                return HttpResponseRedirect(redirect_to)
        elif request.POST.get("forgetP"):
            return render(request, 'registration/password_reset_form.html')
        else:
            error_type = 4
            return render(request, 'error_page.html', {'t': error_type})

    form = authentication_form(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required(login_url="/accounts/login/")
def profile(request):
    # This code allows for an admin link on the user profile page.
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None

    folders = profile.folder_set.all()[:20]

    if len(folders) == 0:
        folder = Folder()
        folder.owner = profile
        folder.save()
        # folders = Folder.objects.all()[:20]

    root_folder = profile.folder_set.filter(file_name="DEFAULT FOLDER")[0]
    return render(request, 'user_profile.html', {'o': root_folder, 'prof': profile})


@login_required(login_url="/accounts/login/")
def report_list(request, folder_id):
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        error_type = 3
        return render(request, 'error_page.html', {'t': error_type})

    folders = profile.folder_set.all()
    if folders.filter(pk=folder_id):
        return render(request, 'report_list.html', {'folder': folders.filter(pk=folder_id)[0]})
    else:
        error_type = 3
        return render(request, 'error_page.html', {'t': error_type})


@login_required(login_url="/accounts/login/")
def add_folder(request):
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None

    if request.method == 'POST':
        title = request.POST.get("file_name")
        name_line = request.POST.get("parent_folder").split("/")
        parent_id = name_line[1]

        # handel invalid input
        if len(title) == 0:
            error = "Error: folder name needed!"
            folders = profile.folder_set.all()[:20]
            return render(request, 'add_folder.html', {'folder': folders, 'message': error})
        else:
            parent = profile.folder_set.get(pk=parent_id)
            if parent.parents.filter(file_name=title).count() != 0:
                error = "Error: folder already exist in directory " + parent.file_name
                folders = profile.folder_set.all()[:20]
                return render(request, 'add_folder.html', {'folder': folders, 'message': error})
            else:
                folder = Folder(file_name=title, parent_folder=parent, owner=profile)
                folder.save()

        root_folder = profile.folder_set.filter(file_name="DEFAULT FOLDER")[0]

        return HttpResponseRedirect(reverse('accounts:profile'))

    folders = profile.folder_set.all()[:20]
    error = ""
    return render(request, 'add_folder.html', {'folder': folders, 'message': error})


@login_required(login_url="/accounts/login/")
def edit_folder(request, folder_id):
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        error_type = 3
        return render(request, 'error_page.html', {'t': error_type})

    if len(profile.folder_set.filter(pk=folder_id)) == 0:
        error_type = 3
        return render(request, 'error_page.html', {'t': error_type})
    else:
        current_folder = profile.folder_set.filter(pk=folder_id)[0]
        folders = profile.folder_set.all()[:20]

        if request.method == 'POST':
            # handle different request
            if request.POST.get("cancel"):  # Cancel
                return HttpResponseRedirect(reverse('accounts:report_list', args=[folder_id]))
            elif request.POST.get("save"):  # Save changes
                title = request.POST.get("file_name")
                name_line = request.POST.get("parent_folder").split("/")
                parent_id = name_line[1]
                parent = profile.folder_set.get(pk=parent_id)
                if parent.parent_folder == current_folder:
                    error = "Error: Your target folder " + parent.file_name + "is  currently in " + current_folder.file_name
                    return render(request, 'edit_folder.html',
                              {'current': current_folder, 'folder': folders, 'message': error})
                elif parent == current_folder:
                    error = "Error: You are trying to put " + current_folder.file_name + " in itself!"
                    return render(request, 'edit_folder.html',
                              {'current': current_folder, 'folder': folders, 'message': error})
                elif len(title) == 0:
                    current_folder.parent_folder = parent
                    current_folder.save()
                    return HttpResponseRedirect(reverse('accounts:report_list', args=[folder_id]))
                elif parent.parents.filter(file_name=title).count() != 0:
                    error = "Error: Folder " + title + " already exist in the target folder " + parent.file_name
                    return render(request, 'edit_folder.html',
                              {'current': current_folder, 'folder': folders, 'message': error})
                else:
                    current_folder.file_name = title
                    current_folder.parent_folder = parent
                    current_folder.save()
                    return HttpResponseRedirect(reverse('accounts:report_list', args=[folder_id]))
            elif request.POST.get("delete"):  # Delete folder
                get_object_or_404(Folder, pk=folder_id).delete()
                root_folder = profile.folder_set.filter(file_name="DEFAULT FOLDER")[0]
                return HttpResponseRedirect(reverse('accounts:profile'))
            else:  # only for debug issue
                error = "Error: button not working!"
                return render(request, 'edit_folder.html', {'current': current_folder, 'folder': folders, 'message': error})

    error = ""
    return render(request, 'edit_folder.html', {'current': current_folder, 'folder': folders, 'message': error})


def admin_page(request):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    Groups = UserGroup.objects.all()[:20]
    Users = UserProfile.objects.all()[:20]

    context = {'groups': Groups, 'users': Users}
    return render(request, 'admin/main.html', context)


def admin_user(request, user_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    u = UserProfile.objects.filter(pk=user_id)[0]

    context = {'u': u, 'isnotme': u.user != request.user}
    return render(request, 'admin/user.html', context)


def admin_group(request, group_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    user_set = UserProfile.objects.filter(user__groups=UserGroup.objects.filter(pk=group_id)[0].group)

    context = {'g': UserGroup.objects.filter(pk=group_id)[0], 'user_set': user_set}
    return render(request, 'admin/group.html', context)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def admin_creategroup(request, creation_form=GroupCreationForm):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    if request.method == "POST":
        form = creation_form(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/admin")
    else:
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


def admin_suspend(request, user_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    u = UserProfile.objects.filter(pk=user_id)[0]
    u.suspended = 1
    u.user.save()
    u.save()
    return render(request, 'admin/action_complete.html')


def admin_unsuspend(request, user_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    u = UserProfile.objects.filter(pk=user_id)[0]
    u.suspended = 0
    u.user.save()
    u.save()
    return render(request, 'admin/action_complete.html')


def admin_group_adduser(request, group_id, addition_form=GroupAdditionForm):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    if request.method == "POST":
        form = addition_form(data=request.POST)
        if form.is_valid():
            user = form.save()
            group = UserGroup.objects.filter(pk=group_id)[0]
            group.group.user_set.add(user)
            group.save()
            group.group.save()
            return HttpResponseRedirect("/accounts/admin")
    else:
        form = addition_form(request)

    context = {
        'form': form,
        'g': UserGroup.objects.filter(pk=group_id)[0]
    }
    return render(request, "admin/group_adduser.html", context)


def admin_group_removeuser(request, group_id, user_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    g = UserGroup.objects.filter(pk=group_id)[0]
    u = UserProfile.objects.filter(pk=user_id)[0].user
    g.user_set.remove(u)
    g.save()
    return render(request, 'admin/action_complete.html')


def admin_group_delete(request, group_id):
    if check_user_fail(request):
        return render(request, 'admin/reject.html')

    g = UserGroup.objects.filter(pk=group_id)[0]
    g.group.delete()
    g.delete()
    return render(request, 'admin/action_complete.html')


def check_user_fail(request):
    try:
        profile = UserProfile.objects.filter(user=request.user)[0]
    except IndexError:
        return True
    if not profile.is_admin:
        return True


@login_required(login_url="/accounts/login/")
def add_group(request, creation_form=UserGroupCreationForm):
    if request.method == "POST":
        form = creation_form(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = creation_form(request)
    context = {
        'form': form,
    }
    return render(request, "add_group.html")
