from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())

class UserRegisterForm(forms.Form):
    f_name = forms.CharField(label='First name', max_length=100)
    l_name = forms.CharField(label='Last name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', max_length=100)

