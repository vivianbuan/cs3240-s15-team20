from django.conf.urls import patterns, include, url
from django.contrib import admin, auth
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'Report.views.home', name='home'),
    url(r'^reports/', include('Report.urls', namespace="reports"), name='reports'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^messages/', include('SiteMail.urls', namespace="mails"), name='mails'),
    url(r'^accounts/', include('accounts.urls', namespace="accounts"), name='accounts'),) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

