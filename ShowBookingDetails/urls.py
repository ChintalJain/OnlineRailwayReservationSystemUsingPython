from django.urls import path
from ShowBookingDetails.views import showTicket_view,showTicket_validate

urlpatterns=[
	path('showTicketDetails/',showTicket_view),
	path('validateshowTicketDetails/',showTicket_validate),
]
