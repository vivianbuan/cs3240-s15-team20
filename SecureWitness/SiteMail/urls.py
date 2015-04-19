from django.conf.urls import patterns, include, url

from SiteMail import views

urlpatterns = patterns('',
                       url(r'^$', views.mail_list, name='inbox'),
                       url(r'^content/(\d+)/$', views.mail_detail, name='mail_detail'),
                       url(r'^compose_mail/$', views.compose, name='compose_mail'),

)