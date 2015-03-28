from django.conf.urls import patterns, include, url
from django.contrib import admin, auth

urlpatterns = patterns('',
    url(r'^$', 'Report.views.home', name='home'),
    url(r'^detail/(\d+)/$', 'Report.views.detail', name='detail'),
    )
