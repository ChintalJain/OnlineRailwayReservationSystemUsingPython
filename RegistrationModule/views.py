from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from RegistrationModule.models import UserDetails,LoginDetails
import re
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def registration_view(request):
	c={}
	c.update(csrf(request))
	return render_to_response('registration.html',c)

def auth_registration(request):
	username=request.POST.get('username','')
	password=request.POST.get('password','')
	confpass=request.POST.get('confpass','')
	fname=request.POST.get('firstname','')
	lname=request.POST.get('lastname','')
	gender=request.POST.get('gender','')
	dob=request.POST.get('dateofbirth','')
	cno=request.POST.get('contactnumber','')
	email=request.POST.get('emailid','')

	isValid=True

	if(len(username)<6 or len(username)>10):
		isValid=False
		msg="Username should be of length 6-10"
	
	RegexForPassword0=r'[A-Za-z0-9@#$%&!]{10}'
	RegexForPassword1=r'[@#$%&!]{10}'
	RegexForPassword2=r'[0-9]{10}'
	RegexForPassword3=r'[A-Za-z]{10}'
	if(len(password)==10):
		pattern0=re.compile(RegexForPassword0)
		pattern1=re.compile(RegexForPassword1)
		pattern2=re.compile(RegexForPassword2)
		pattern3=re.compile(RegexForPassword3)

		if(re.match(pattern1,password) or re.match(pattern2,password) or re.match(pattern3,password)):
			isValid=False
			msg="Password should be combination of letters digits and special characters."
		elif(re.match(pattern0,password)):
			if(password!=confpass):
				isValid=False
				msg="Password & Confirm password Must be same."
		else:
			isValid=False
			msg="Password should be combination of letters digits and special characters."
	else:
		isValid=False
		msg="Password must be of length 10."
		
	RegexForContactNumber=r'[0-9]{10}'
	pattern=re.compile(RegexForContactNumber)
	if(not re.match(pattern,cno)):
		isValid=False
		msg="Please enter valid contact number."
	
	RegexForEmail=r'\S+@([a-z]+)((\.([a-z]+))+)'	
	pattern=re.compile(RegexForEmail)
	if(not re.match(pattern,email)):
		isValid=False
		msg="Please enter valid email id."

	c={}
	c.update(csrf(request))
		
	if isValid:
		try:
			user=UserDetails.objects.get(username=username)
		except ObjectDoesNotExist:
			l=LoginDetails(username=username,password=password)
			u=UserDetails(username=username,password=password,f_name=fname,l_name=lname,gender=gender,dob=dob,contact_number=cno,email=email)
			u.save()
			l.save()
			return HttpResponseRedirect('/loginModule/loginPage/',c)
		else:
			msg="This Username already exist....Try with different username."
			c.update({"errorMsg":msg})		
			return render_to_response('invalidRegistration.html',c)	
	else:
		c.update({"errorMsg":msg})		
		return render_to_response('invalidRegistration.html',c)
