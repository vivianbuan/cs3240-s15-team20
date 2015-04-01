from django.conf.urls import patterns, include, url
from django.contrib import admin, auth

urlpatterns = patterns('Report.views',
    url(r'^$', 'home', name='home'),
    url(r'^detail/(\d+)/$', 'detail', name='detail'),
    url(r'^add_report/$', 'add_report', name='add_report'),
    url(r'^folder/$', 'show_in_folder', name='folder_name')
	url(r'^', include('fileUpload.urls')),
)
