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


def home(request):
    entries = reports.objects.all()[:20]
    return render(request, 'index.html', {'report': entries})


def detail(request, pk):
	rep = reports.objects.all().filter(pk=pk)[0]
	doc = Document.objects.all().filter(report = rep)
	return render(request, 'detail.html', {'report': rep, 'documents': doc})

def add_report(request):
	if request.method == 'POST':
		auth = request.POST.get("author")
		sh = request.POST.get("short")
		det = request.POST.get("details")
		loc = request.POST.get("location")
		d = request.POST.get("date")
		if d == "": 
			d = None
		keys = request.POST.get("keywords")
		priv = request.POST.get("private", False)
		rep = reports(author = auth, short = sh, details = det, location = loc, date = d, keywords = keys, private = priv)
		rep.save()

		files = request.FILES.getlist('files[]')
		for f in files: 
			doc = Document(docfile = f, report = rep)
			doc.save()

		# Redirect to home
		entries = reports.objects.all()[:20]
		return render(request, 'index.html', {'report': entries})
		
	entries = reports.objects.all()[:20]

	return render(request,'add_report.html', {'report': entries})

