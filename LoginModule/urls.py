from django.urls import path
from LoginModule.views import login_view,auth_login

urlpatterns=[
	path('loginPage/',login_view),
	path('authLogin/',auth_login),
]
