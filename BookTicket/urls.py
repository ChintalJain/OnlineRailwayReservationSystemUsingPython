from django.urls import path
from BookTicket.views import home_view,showtrain_view,train_view,booking_view,booking_details

urlpatterns=[
	path('homePage/',home_view),
	path('showTrains/',showtrain_view),
	path('trains/',train_view),
	path('finalBooking/',booking_view),
	path('bookingDetails/',booking_details),
]
