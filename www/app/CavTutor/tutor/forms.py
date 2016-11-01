from django import forms

max_length=100
widget=forms.PasswordInput()

MY_INSTS = ( ('1','UVA'), ('2', 'Virginia Tech'))
MY_COURSES = ( ('1','CS 4144'), ('2', 'CS 1501'))

class TutorRegisterForm(forms.Form):
	institution = forms.ChoiceField(choices=MY_INSTS)
	course = forms.ChoiceField(choices=MY_COURSES)

