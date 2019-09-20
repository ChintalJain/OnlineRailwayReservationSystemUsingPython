from django.urls import path
from CancelTicket.views import cancel_view,cancel_validate

urlpatterns=[
	path('ticketCancellation/',cancel_view),
	path('validateCancellation/',cancel_validate),
]
