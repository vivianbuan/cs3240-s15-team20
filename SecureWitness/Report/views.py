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
    return render(request, 'detail.html', {'report': reports.objects.all().filter(pk=pk)[0]})



def add_report(request):
	if request.method == 'POST':
		# Handle files
		files = request.FILES.getlist('files[]')
		for f in files: 
			doc = Document(docfile = f)
			doc.save()

		pprint(request, sys.stderr)

		# Create and save report 
		auth = request.POST.get("author")
		t = request.POST.get("title")
		sh = request.POST.get("short")
		det = request.POST.get("details")
		loc = request.POST.get("location")
		d = request.POST.get("date")
		if d == "": 
			d = None
		keys = request.POST.get("keywords")
		f = None
		priv = request.POST.get("private", False)
		report = reports(author = auth, title = t, short = sh, details = det, location = loc, date = d, keywords = keys, private = priv)
		report.save()

		documents = Document.objects.all()
		# Redirect to home
		return render(request, 'fileUpload/list.html', {'documents': documents})
		
	entries = reports.objects.all()[:20]

	return render(request,'add_report.html', {'report': entries})
