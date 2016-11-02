from django import forms
from core.settings import UX_BASE 

import requests, json
    
def get_all_courses():
    courses = requests.get(UX_BASE + 'courses/')

    for course in courses.json():
        selector_id = course['id']
        selector_label = "{} at {}".format(course['abbr'], course['institution_name'])
        
        yield selector_id, selector_label

class TutorCreateForm(forms.Form):
    course = forms.ChoiceField(choices=get_all_courses())
    rate = forms.DecimalField(max_digits=16, decimal_places=2, label="Rate (USD$)")
    
