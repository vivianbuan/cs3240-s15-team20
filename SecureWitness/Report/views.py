from django.shortcuts import render
from Report.models import reports


def home(request):
    entries = reports.objects.all()[:20]

    return render(request, 'index.html', {'report': entries})


def detail(request, pk):
	return render(request, 'detail.html', {'report': reports.objects.all().filter(pk=pk)[0]})