from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from RegistrationModule.models import LoginDetails
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def login_view(request):
	c={}
	c.update(csrf(request))
	return render_to_response('loginPage.html',c)

def auth_login(request):
	username=request.POST.get('username','')
	password=request.POST.get('password','')

	c={}
	c.update(csrf(request))
	try:
		user=LoginDetails.objects.get(username=username)
	except ObjectDoesNotExist:
		msg="INVALID CREDENTIAL....      PLEASE TRY AGAIN..."
		c.update({"errorMsg":msg})		
		return render_to_response('invalidLogin.html',c)	
	else:
		if user is not None and user.password==password:
			request.session['username']=username
			return HttpResponseRedirect('/bookTicket/homePage/',c)
		else:
			msg="INVALID CREDENTIAL....      PLEASE TRY AGAIN..."
			c.update({"errorMsg":msg})		
			return render_to_response('invalidLogin.html',c)	
