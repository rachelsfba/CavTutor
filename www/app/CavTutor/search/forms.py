from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Query', max_length=256)



