from django import forms
from django.forms import ModelForm
from Report.models import Folder


class AddReportForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title', 'name': 'title'}))
    short_description = forms.CharField(max_length=100)
    long_description = forms.CharField()
    docfile = forms.FileField(label='Select a file')


class AddFolderForm(forms.Form):
    file_name = forms.CharField(max_length=100)
    parent_folder = forms.ModelChoiceField(queryset=Folder.objects.all())