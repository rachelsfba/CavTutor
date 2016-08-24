from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	context = {
		'body_text': 'Hello, world. This is the main page of the Internet Scale Appliations Project No. 1.',
	}
	return render(request, 'home/index.html', context)
