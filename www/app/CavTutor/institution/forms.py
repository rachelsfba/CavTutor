from django import forms

class InstitutionCreateForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    abbr = forms.CharField(label='Abbr', max_length=16)
    address = forms.CharField(label='Address', max_length=256)
