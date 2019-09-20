from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf

# Create your views here.

def logout_view(request):
	c={}
	c.update(csrf(request))
	try:
		request.session['username']
	except KeyError:
		return HttpResponseRedirect('/loginModule/loginPage/',c)
	else:
		del request.session['username']
		return HttpResponseRedirect('/loginModule/loginPage/',c)