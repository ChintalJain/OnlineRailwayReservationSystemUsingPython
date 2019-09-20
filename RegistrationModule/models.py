from django.db import models

# Create your models here.

class UserDetails(models.Model):
	username=models.CharField(max_length=10,primary_key=True)
	password=models.CharField(max_length=10)
	f_name=models.CharField(max_length=20)
	l_name=models.CharField(max_length=20)
	gender=models.CharField(max_length=6)
	dob=models.CharField(max_length=10)
	contact_number=models.CharField(max_length=10)
	email=models.CharField(max_length=30)

class LoginDetails(models.Model):
	username=models.CharField(max_length=10,primary_key=True)
	password=models.CharField(max_length=10)
