from django.conf.urls import patterns, include, url
from django.contrib import admin, auth

urlpatterns = patterns('Report.views',
    url(r'^$', 'home', name='home'),
    url(r'^detail/(\d+)/$', 'detail', name='detail'),
    url(r'^delete/(\d+)/$', 'delete', name='delete'),
    url(r'^edit/(\d+)/$', 'edit', name='edit'),
    url(r'^add_report/$', 'add_report', name='add_report'),
)
