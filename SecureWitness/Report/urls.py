from django.conf.urls import patterns, include, url
from django.contrib import admin, auth

urlpatterns = patterns('',
    url(r'^$', 'Report.views.home', name='home'),
    url(r'^detail/(\d+)/$', 'Report.views.detail', name='detail'),
    url(r'^add_report/$', 'Report.views.add_report', name='add_report'),
#    url(r'^foler/$', 'Report.views.show_in_folder', name='folder_name')
    )
