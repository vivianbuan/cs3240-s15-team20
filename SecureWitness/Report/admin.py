from django.contrib import admin
from Report.models import reports


#class ReportAdmin(admin.ModelAdmin):
#    fields = ['author', 'title']



admin.site.register(reports)
