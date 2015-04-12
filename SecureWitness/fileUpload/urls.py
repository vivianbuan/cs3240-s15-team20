# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('fileUpload.views', url(r'^list/$', 'list', name='list'),)
