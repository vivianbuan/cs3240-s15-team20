from django.shortcuts import render
from accounts.models import UserProfile
from SiteMail.models import Mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="/accounts/login/")
def mail_list(request):
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None

    mails = profile.receive_mails.order_by('-date')
    return render(request, 'mail.html', {'mail': mails, 'prof': profile})


@login_required(login_url="/accounts/login/")
def mail_detail(request, pk):
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None

    mail = profile.receive_mails.get(pk=pk)
    return render(request, 'mail_detail.html', {'m': mail, 'prof': profile})


@login_required(login_url="/accounts/login/")
def compose(request):
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None

    if request.method == 'POST':
        recipient_name = request.POST.get("recipient")
        user_query = UserProfile.objects.filter(user__username=recipient_name)
        if user_query:
            recipient_user = UserProfile.objects.filter(user__username=recipient_name)[0]
            auth = profile
            sub = request.POST.get("subject")
            con = request.POST.get("content")

            new_mail = Mail(title=sub, details=con, from_user=auth, to_user=recipient_user)
            new_mail.save()

            mails = profile.receive_mails.all()[:20]
            return render(request, 'mail.html', {'mail': mails, 'prof': profile})
        else:
            error = "Error: the recipient does not exist!"
            return render(request, 'compose_mail.html', {'prof': profile, 'message': error})

    return render(request, 'compose_mail.html', {'prof': profile})