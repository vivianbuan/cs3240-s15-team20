from django.shortcuts import render_to_response
from django.shortcuts import render
from Report.models import reports
from Report.models import Document
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from Report.models import Folder


def home(request):
    entries = reports.objects.all()[:20]
    folders = Folder.objects.all()[:20]

    return render(request, 'index.html', {'report': entries})
#    return render(request, 'index.html', {'folder': folders})


def detail(request, pk):
	return render(request, 'detail.html', {'report': reports.objects.all().filter(pk=pk)[0]})

def add_report(request):
	if request.method == 'POST':
		# Handle files
		files = request.FILES.getlist('files[]')
		for f in files: 
			doc = Document(docfile = f)
			doc.save()

		documents = Document.objects.all()
		# Redirect to home
		return render(request, 'fileUpload/list.html', {'documents': documents})
		
	entries = reports.objects.all()[:20]

	return render(request,'add_report.html', {'report': entries})

def show_in_folder(request):
#    reports_list = reports.objects.order_by('-timestamp')[:5]
#    context = {'reports_list': reports_list}
#    return render(request, 'report_list.html', context)
	pass
