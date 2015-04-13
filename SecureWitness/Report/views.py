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



def home(request):
    entries = reports.objects.all().filter(private=False)[:20]
    return render(request, 'index.html', {'report': entries})


def detail(request, pk):
	rep = reports.objects.all().filter(pk=pk)[0]
	doc = Document.objects.all().filter(report = rep)
	return render(request, 'detail.html', {'report': rep, 'documents': doc})



def delete(request, pk): 
	if request.method == 'POST': 
		rep = reports.objects.all().filter(pk=pk)[0]
		doc = Document.objects.all().filter(report = rep)

		rep.delete()
		for docs in doc: 
			docs.delete()

		
	entries = reports.objects.all().filter(private=False)[:20]
	return render(request, 'index.html', {'report': entries})


def edit(request, pk): 
	# Retrieve the right report
	rep = reports.objects.all().filter(pk=pk)[0]
	doc = Document.objects.all().filter(report = rep)
	
	if request.method == 'POST': 
		# Get possible changes from the form		
		auth = request.POST.get("author")
		sh = request.POST.get("short") 
		det = request.POST.get("details")
		loc = request.POST.get("location")
		keys = request.POST.get("keywords")
		d = request.POST.get("date")		
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
				document = Document(docfile = f, report = rep)
				document.save() 
			
			doc = Document.objects.all().filter(report = rep)
			return render(request, 'detail.html', {'report': rep, 'documents': doc})

	return render(request, 'edit.html', {'report': rep, 'documents': doc})

@login_required(login_url="/accounts/login/")
def add_report(request):
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
		rep = reports(author = auth, short = sh, details = det, location = loc, date = d, keywords = keys, private = priv)
		rep.save()
		# Save Files associated to the report
		files = request.FILES.getlist('files[]')
		for f in files: 
			doc = Document(docfile = f, report = rep)
			doc.save()

		# Redirect to home
		entries = reports.objects.all().filter(private=False)[:20]
		return render(request, 'index.html', {'report': entries})
		
	entries = reports.objects.all()[:20]

	return render(request,'add_report.html', {'report': entries})
