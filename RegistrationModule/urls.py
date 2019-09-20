from django.urls import path
from RegistrationModule.views import registration_view,auth_registration

urlpatterns=[
	path('register/',registration_view),
	path('authRegistration/',auth_registration),
]
