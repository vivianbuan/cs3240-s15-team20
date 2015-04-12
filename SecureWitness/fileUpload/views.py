# -*- coding: utf-8 -*-
import sys 
from pprint import pprint
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from fileUpload.models import Document

def list(request): 
	# Handle file upload
	if request.method == 'POST': 
		files = request.FILES.getlist('files[]')
		for f in files: 
			doc = Document(docfile = f)
			doc.save()

		# Redirect to the document list after POST 
		return HttpResponseRedirect(reverse('fileUpload.views.list'))

	# Load documents for the list page
	documents = Document.objects.all()

	# Render list page with the documents and the form
	return render_to_response('fileUpload/list.html', {'documents': documents}, context_instance=RequestContext(request))
