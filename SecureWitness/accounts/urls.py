from django.conf.urls import patterns, include, url

from accounts import views


urlpatterns = patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^changepw/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/folder/(\d+)/$', views.report_list, name='report_list'),
    url(r'^profile/folder/(\d+)/edit$', views.edit_folder, name='edit_folder'),
    url(r'^profile/add_folder$', views.add_folder, name='add_folder'),
    url(r'^admin/$', views.admin_page, name='admin_page'),
    url(r'^admin/user/(\d+)/$', views.admin_user, name='admin_user'),
    url(r'^admin/delete/user/(\d+)/$', views.admin_deleteuser, name='admin_deleteuser'),
    url(r'^admin/modify/user/(\d+)/$', views.admin_makeadmin, name='admin_makeadmin'),
    url(r'^admin/group/(\d+)/$', views.admin_group, name='admin_group'),
    url(r'^admin/group/$', views.admin_creategroup, name='admin_creategroup'),
    url(r'^admin/group/adduser/$', views.admin_group_adduser, name='admin_group_adduser'),
    url(r'^add_group/$', views.add_group, name='add_group'),
)