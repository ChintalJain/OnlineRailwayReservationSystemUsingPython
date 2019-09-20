from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from BookTicket.models import TimeTable,TrainBooked,CoachDetails,BookingPrice,TrainDetails,Station,BookedTicketDetails,PassengerDetails
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def showTicket_view(request):
	c={}
	c.update(csrf(request))
	try:
		request.session['username']
	except KeyError:
		return HttpResponseRedirect('/loginModule/loginPage/',c)
	else:
		return render_to_response('showTicket.html',c)

def showTicket_validate(request):
	c={}
	c.update(csrf(request))
	try:
		request.session['username']
	except KeyError:
		return HttpResponseRedirect('/loginModule/loginPage/',c)
	else:
		pnr=request.POST.get('pnr_number','')
		if(len(pnr)!=9):
			msg="PNR Number Should Be Of Length 9..."
			c.update({'errorMsg':msg})
			return render_to_response('invalidshowTicket.html',c)

		try:
			t=BookedTicketDetails.objects.get(PNRno=pnr)
		except ObjectDoesNotExist:
			msg="PLEASE ENTER VALID PNR NUMBER...."
			c.update({'errorMsg':msg})
			return render_to_response('invalidshowTicket.html',c)
		else:
			t=BookedTicketDetails.objects.get(PNRno=request.POST.get('pnr_number',''))
			p=PassengerDetails.objects.filter(PNRno=t)
			
			plist=list(p)
			
			c.update({'ticket':t})
			c.update({'plist':plist})
			
			sourceStation=Station.objects.get(stationId=t.source)
			destiniStation=Station.objects.get(stationId=t.destination)
			source=TimeTable.objects.get(trainNo=t.trainNo,stationID=sourceStation)
			destination=TimeTable.objects.get(trainNo=t.trainNo,stationID=destiniStation)
			
			c.update({'source':source})			
			c.update({'destination':destination})

			return render_to_response('ticketDetails.html',c)