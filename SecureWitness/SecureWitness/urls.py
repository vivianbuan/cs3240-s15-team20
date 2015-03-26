from django.conf.urls import patterns, include, url
from django.contrib import admin, auth

urlpatterns = patterns('',
    url(r'^$', 'Report.views.home', name='home'),
    url(r'^reports/', include('Report.urls',namespace="reports"), name='reports'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls',namespace="accounts"), name='accounts'),
    )
