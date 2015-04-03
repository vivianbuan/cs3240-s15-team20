from django.conf.urls import patterns, include, url

from accounts import views


urlpatterns = patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^changepw/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/folder/(\d+)/$', views.report_list, name='report_list'),
)