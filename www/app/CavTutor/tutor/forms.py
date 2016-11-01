from django import forms
from core.settings import UX_BASE 

from urllib.request import urlopen
from urllib.parse import urlencode
import json


max_length=100
widget=forms.PasswordInput()

def getCourses():

	json_data = urlopen(UX_BASE + 'courses/').read().decode('utf-8')#json_data = requests.get(UX_BASE + 'tutors/').json()
	dictobj = json.loads(json_data)#return dictobj
	l=[]
	for course in dictobj:
		l.append( (course['id'],course['name']+" ("+course['abbr']+")"+" at "+course['institution_name']))
	return tuple(l)
    #MY_COURSES = ( ('1','CS 4144 at UVA'), ('2', 'CS 1501 at VA Tech'))
    #return MY_COURSES

class TutorRegisterForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(TutorRegisterForm, self).__init__(*args, **kwargs)

		
		allcourses = getCourses()
		#MY_COURSES = ( ('1','CS 4144 at UVA'), ('2', 'CS 1501 at VA Tech'))
		self.fields['course'] = forms.ChoiceField(choices=allcourses)

		self.fields['adv_rate'] = forms.DecimalField(max_digits=16, decimal_places=2)
