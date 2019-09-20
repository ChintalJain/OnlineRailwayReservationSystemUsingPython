from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from BookTicket.models import BookedTicketDetails,PassengerDetails,TrainBooked
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def cancel_view(request):
	c={}
	c.update(csrf(request))
	try:
		request.session['username']
	except KeyError:
		return HttpResponseRedirect('/loginModule/loginPage/',c)
	else:
		return render_to_response('cancelTicket.html',c)

def cancel_validate(request):
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
			return render_to_response('invalidcancelTicket.html',c)

		try:
			t=BookedTicketDetails.objects.get(PNRno=pnr)
		except ObjectDoesNotExist:
			msg="PLEASE ENTER VALID PNR NUMBER...."
			c.update({'errorMsg':msg})
			return render_to_response('invalidcancelTicket.html',c)
		else:
			if t.username!=request.session['username']:	
				msg="PLEASE ENTER VALID PNR NUMBER...."
				c.update({'errorMsg':msg})
				return render_to_response('invalidcancelTicket.html',c)
			else:
				p=PassengerDetails.objects.filter(PNRno=t)
				tb=TrainBooked.objects.get(date=t.doj_id)
				tseat=0
				plist=list(p)
				cl=plist[0].coachNo[0:2]
				refund=t.totalPrice
				for x in p:
					tseat=tseat+1
				if cl=='CC':
					tb.availableCC=tb.availableCC+tseat
					if refund > 120:
						refund=refund-tseat*120
					else:
						refund=0
				else:
					tb.available2S=tb.available2S+tseat
					if refund > 60:
						refund=refund-tseat*60
					else:
						refund=0
				tb.save()
				t.delete()
				c.update({'pnr':pnr})
				c.update({'tp':refund})				

				return render_to_response('confirmCancel.html',c)