from django.urls import path
from LogoutModule.views import logout_view

urlpatterns=[
	path('logout/',logout_view),
]
