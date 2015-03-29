from django.contrib import admin
from Report.models import reports
from Report.models import Folder


#class ReportAdmin(admin.ModelAdmin):
#    fields = ['author', 'title']



admin.site.register(reports)
admin.site.register(Folder)
