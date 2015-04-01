from django import forms

class AddReportForm(forms.Form): 
	title = forms.CharField(label='Title', max_lenght=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'name': 'title'})
	short_description = forms.CharField(max_length=100)
	long_description = forms.CharField()
	docfile = forms.FileField(label='Select a file')
