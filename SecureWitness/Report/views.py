from django.shortcuts import render_to_response

from Report.models import reports


def home(request):
    entries = reports.objects.all()[:20]

    return render_to_response('index.html', {'report': entries})


def detail(request, pk):
	return render_to_response('detail.html', {'report': reports.objects.all().filter(pk=pk)[0]})