from django.shortcuts import render,render_to_response
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
import datetime,random
from BookTicket.models import TimeTable,TrainBooked,CoachDetails,BookingPrice,TrainDetails,Station,BookedTicketDetails,PassengerDetails
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def home_view(request):
	c={}
	c.update(csrf(request))
	try:
		request.session['username']
	except KeyError:
		return HttpResponseRedirect('/loginModule/loginPage/',c)
	else:
		return render_to_response('homePage.html',c)

def showtrain_view(request):
	c={}
	c.update(csrf(request))
	try:
		request.session['username']
	except KeyError:
		return HttpResponseRedirect('/loginModule/loginPage/',c)
	else:
		return render_to_response('showTrains.html',c)

def train_view(request):
	c={}
	c.update(csrf(request))
	try:
		request.session['username']
	except KeyError:
		return HttpResponseRedirect('/loginModule/loginPage/',c)
	else:
		source=request.POST.get('from','')
		destination=request.POST.get('to','')
		doj=request.POST.get('doj','')
		
		if(source==destination):
			msg="Please Enter Proper Sourse And Destination.."
			c.update({'errorMsg':msg})
			return render_to_response('invalidshowTrains.html',c)
					
		now=datetime.datetime.now()

		if(int(doj[5:7]) < now.month or int(doj[8:]) < now.day or int(doj[0:4]) < now.year):
			msg="Please Enter Proper Date.."
			c.update({'errorMsg':msg})
			return render_to_response('invalidshowTrains.html',c)

		trainsFromS=TimeTable.objects.filter(stationID=source)
		trainsToD=TimeTable.objects.filter(stationID=destination)					  
		count=0
		trainList=[]
		for i in trainsFromS:
			for j in trainsToD:
				if i.trainNo==j.trainNo and i.id<j.id:
					try:
						price=BookingPrice.objects.get(stationId1=source,stationId2=destination)
					except ObjectDoesNotExist:
						price=BookingPrice.objects.get(stationId2=source,stationId1=destination)
			
					try:
						booked=TrainBooked.objects.get(date=doj,trainNo=i.trainNo)
					except ObjectDoesNotExist:
						coach=CoachDetails.objects.get(id=1)
						if i.trainNo.trainType=='Express' :
							trainList.append([i.trainNo.trainNo,i.trainNo.trainName,i.trainNo.trainType,i.stationID.statinName,i.arrival,i.departure,j.stationID.statinName,j.arrival,j.departure,coach.coachCC * i.trainNo.noOfCCCoach,coach.coach2S * i.trainNo.noOf2SCoach,price.coachCC,price.coach2S])
						else:
							trainList.append([i.trainNo.trainNo,i.trainNo.trainName,i.trainNo.trainType,i.stationID.statinName,i.arrival,i.departure,j.stationID.statinName,j.arrival,j.departure,coach.coachCC * i.trainNo.noOfCCCoach,coach.coach2S * i.trainNo.noOf2SCoach,price.coachCC+45,price.coach2S+15])	
					else:
						if i.trainNo.trainType=='Express' :
							trainList.append([i.trainNo.trainNo,i.trainNo.trainName,i.trainNo.trainType,i.stationID.statinName,i.arrival,i.departure,j.stationID.statinName,j.arrival,j.departure,booked.availableCC,booked.available2S,price.coachCC,price.coach2S])					
						else:
							trainList.append([i.trainNo.trainNo,i.trainNo.trainName,i.trainNo.trainType,i.stationID.statinName,i.arrival,i.departure,j.stationID.statinName,j.arrival,j.departure,booked.availableCC,booked.available2S,price.coachCC+45,price.coach2S+15])
					count=count+1

		if(count==0):
			msg="There is no train between These 2 stations.."
			c.update({'errorMsg':msg})
			return render_to_response('invalidshowTrains.html',c)
		else:
			request.session['source']=source
			request.session['destination']=destination
			request.session['doj']=doj
			c.update({'trainDetails':trainList})
			return render_to_response('trains.html',c)

def booking_view(request):
	c={}
	c.update(csrf(request))
	try:
		request.session['username']
	except KeyError:
		return HttpResponseRedirect('/loginModule/loginPage/',c)
	else:
		try:
			request.session['source']
			request.session['destination']
			request.session['doj']
		except KeyError:
			return HttpResponseRedirect('/bookTicket/showTrains/',c)
		else:
			num=request.POST.get('pno','')
			tno=request.GET.get('trainNo','')
			request.session['trainNo']=tno
			request.session['numofp']=num
			list1=[]
			for i in range(0,int(num)):
				list1.append([i+1])
			c.update({'pno':num})
			c.update({'tpno':list1})
			c.update({'tno':tno})
			c.update({'s':request.session['source']})
			c.update({'d':request.session['destination']})
			c.update({'doj':request.session['doj']})
			return render_to_response('finalbooking.html',c)

def booking_details(request):
	c={}
	c.update(csrf(request))
	try:
		request.session['username']
	except KeyError:
		return HttpResponseRedirect('/loginModule/loginPage/',c)
	else:
		try:
			request.session['trainNo']
			request.session['numofp']
		except KeyError:
			return HttpResponseRedirect('/bookTicket/finalBooking/',c)
		else:
			s=request.session['source']
			d=request.session['destination']
			tno=request.session['trainNo']
			doj=request.session['doj']
			pno=request.session['numofp']
			i=TrainDetails.objects.get(trainNo=tno)
			coach=CoachDetails.objects.get(id=1)
			try:
				booked=TrainBooked.objects.get(date=doj,trainNo=i)
			except ObjectDoesNotExist:
				booked=TrainBooked(date=doj,trainNo=i,availableCC=coach.coachCC * i.noOfCCCoach,available2S=coach.coach2S * i.noOf2SCoach)
			flag=True
			while(flag):
				PNR=int(random.randint(800000000,999999999))
				try:
					btd=BookedTicketDetails.objects.get(PNRno=int(PNR))
				except ObjectDoesNotExist:
					break
				else:
					flag=true

			try:
				price=BookingPrice.objects.get(stationId1=s,stationId2=d)
			except ObjectDoesNotExist:
				price=BookingPrice.objects.get(stationId2=s,stationId1=d)
			
			totalPrice=0
			if request.POST.get('class','')=='CC':
				if i.trainType=='Express':
					totalPrice=(price.coachCC)*int(pno)
				else:
					totalPrice=(price.coachCC+45)*int(pno)
			else:
				if i.trainType=='Express':
					totalPrice=(price.coach2S)*int(pno)
				else:
					totalPrice=(price.coach2S+15)*int(pno)
			booked.save()
			t=BookedTicketDetails(PNRno=int(PNR),trainNo=i,source=s,destination=d,totalPrice=totalPrice,username=request.session['username'],doj=booked)
			t.save()
			plist=[]
			for j in range(int(pno)):
				name=request.POST.get('name' + str(j+1),'')
				age=request.POST.get('age' + str(j+1),'')
				gen=request.POST.get('gen' + str(j+1),'')
				
				if request.POST.get('class','')=='CC':
					tseat=coach.coachCC * i.noOfCCCoach
					avail=booked.availableCC
					for x in range(i.noOfCCCoach):
						start=coach.coachCC*x+1	
						end=coach.coachCC*x+coach.coachCC
						if (tseat-avail+1)>=start and (tseat-avail+1)<=end:
							coachNo='CC-'+str(x+1)
							seatNo=tseat-avail+1-coach.coachCC*x
							booked.availableCC=booked.availableCC-1
							break
				else:
					tseat=coach.coach2S * i.noOf2SCoach
					avail=booked.available2S
					for x in range(i.noOf2SCoach):
						start=coach.coach2S*x+1	
						end=coach.coach2S*x+coach.coach2S
						if (tseat-avail+1)>=start and (tseat-avail+1)<=end:
							coachNo='2S-'+str(x+1)
							seatNo=tseat-avail+1-coach.coach2S*x
							booked.available2S=booked.available2S-1
							break
				p=PassengerDetails(name=name,age=age,gender=gen,PNRno=t,coachNo=coachNo,seatNo=seatNo)
				p.save()
				plist.append(p)
			
			booked.save()
			c.update({'ticket':t})
			c.update({'plist':plist})
			
			sourceStation=Station.objects.get(stationId=s)
			destiniStation=Station.objects.get(stationId=d)
			source=TimeTable.objects.get(trainNo=i,stationID=sourceStation)
			destination=TimeTable.objects.get(trainNo=i,stationID=destiniStation)
			
			c.update({'source':source})			
			c.update({'destination':destination})
			
			del request.session['source']
			del request.session['destination']
			del request.session['trainNo']
			del request.session['doj']
			del request.session['numofp']
			
			return render_to_response('bookingdetails.html',c)
						