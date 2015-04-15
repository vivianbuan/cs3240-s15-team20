from django.shortcuts import render_to_response
from django.shortcuts import render
from Report.models import reports
from Report.models import Document
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import sys
from Report.models import Folder
from pprint import pprint
import time
from datetime import date
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
import re
from django.db.models import Q
from django.template import RequestContext


def home(request):
    entries = reports.objects.all().filter(private=False)[:20]
    return render(request, 'index.html', {'report': entries})


def detail(request, pk):
    rep = reports.objects.all().filter(pk=pk)[0]
    doc = Document.objects.all().filter(report=rep)

    # if request.user.is_active:
    #     profile = UserProfile.objects.filter(user=request.user)[0]
    # else:
    #     profile = None
    # folders = profile.folder_set.all()[:20]
    #
    # if request.POST.get("edit"):
    #     return render(request, 'edit.html', {'report': rep, 'documents': doc, 'folder': folders})

    return render(request, 'detail.html', {'report': rep, 'documents': doc})


def delete(request, pk):
    if request.method == 'POST':
        rep = reports.objects.all().filter(pk=pk)[0]
        doc = Document.objects.all().filter(report=rep)

        rep.delete()
        for docs in doc:
            docs.delete()

    entries = reports.objects.all().filter(private=False)[:20]
    return render(request, 'index.html', {'report': entries})

@login_required(login_url="/accounts/login/")
def edit(request, pk):
    # Retrieve the right report
    rep = reports.objects.all().filter(pk=pk)[0]
    doc = Document.objects.all().filter(report=rep)

    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None
    folders = profile.folder_set.all()[:20]

    if request.method == 'POST' and request.POST.get("click"):
        # Get possible changes from the form
        auth = request.POST.get("author")
        sh = request.POST.get("short")
        det = request.POST.get("details")
        loc = request.POST.get("location")
        keys = request.POST.get("keywords")
        d = request.POST.get("date")
        name_line = request.POST.get("parent_folder").split("/")
        parent_id = name_line[1]
        # message = 0
        parent = profile.folder_set.get(pk=parent_id)
        # message = request.POST.get("click")
        if d == "":
            d = None
        priv = request.POST.get("private", False)

        if rep.author == auth:
            # Update the changes
            rep.short = sh
            rep.details = det
            rep.location = loc
            rep.keywords = keys
            rep.date = d
            if priv == "on":
                rep.private = True
            else:
                rep.private = priv
            rep.folder = parent
            # Save the changes
            rep.save()

            # Make changes to existing files
            for d in doc:
                check = request.POST.get(d.docfile.name, False)
                if check or check == "on":
                    d.delete()

            # Upload any new files
            files = request.FILES.getlist('files[]')
            for f in files:
                document = Document(docfile=f, report=rep)
                document.save()

            doc = Document.objects.all().filter(report=rep)
            # return render(request, 'edit.html', {'report': rep, 'documents': doc, 'folder': folders, 'error': message})
            return render(request, 'detail.html', {'report': rep, 'documents': doc})

    # message = request.POST.get("click")
    return render(request, 'edit.html', {'report': rep, 'documents': doc, 'folder': folders})


@login_required(login_url="/accounts/login/")
def add_report(request):
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None

    if request.method == 'POST':
            # Create and save report
        auth = request.POST.get("author")
        sh = request.POST.get("short")
        det = request.POST.get("details")
        loc = request.POST.get("location")
        d = request.POST.get("date")
        if d == "":
            d = None
        keys = request.POST.get("keywords")
        priv = request.POST.get("private", False)

        name_line = request.POST.get("parent_folder").split("/")
        parent_id = name_line[1]
        parent = profile.folder_set.get(pk=parent_id)

        rep = reports(author=auth, short=sh, details=det, location=loc, date=d, keywords=keys, private=priv)
        rep.folder = parent
        rep.save()
        # Save Files associated to the report
        files = request.FILES.getlist('files[]')
        for f in files:
            doc = Document(docfile=f, report=rep)
            doc.save()

        # Redirect to home
        entries = reports.objects.all().filter(private=False)[:20]
        return render(request, 'index.html', {'report': entries})

    entries = reports.objects.all()[:20]
    folders = profile.folder_set.all()[:20]

    return render(request, 'add_report.html', {'report': entries, 'folder': folders})


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):

    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['author', 'details', 'short','keywords',])

        found_entries = reports.objects.filter(entry_query)

    return render_to_response('search.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))

