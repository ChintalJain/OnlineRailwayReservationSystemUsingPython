from django.db import models
# Create your models here.

class TrainDetails(models.Model):
	trainNo=models.CharField(max_length=5,primary_key=True)
	trainName=models.CharField(max_length=30)
	trainType=models.CharField(max_length=10)
	noOfCCCoach=models.IntegerField()
	noOf2SCoach=models.IntegerField()

class Station(models.Model):
	stationId=models.CharField(max_length=5,primary_key=True)
	statinName=models.CharField(max_length=20)
	
class BookingPrice(models.Model):
	stationId1=models.CharField(max_length=5)
	stationId2=models.CharField(max_length=5)
	coach2S=models.IntegerField()
	coachCC=models.IntegerField()

class TrainBooked(models.Model):
	date=models.CharField(max_length=10,primary_key=True)
	trainNo=models.ForeignKey(TrainDetails,on_delete=models.CASCADE)
	availableCC=models.IntegerField()
	available2S=models.IntegerField()
	
class BookedTicketDetails(models.Model):
	PNRno=models.IntegerField(primary_key=True)
	username=models.CharField(max_length=10)
	doj=models.ForeignKey(TrainBooked,on_delete=models.CASCADE)
	trainNo=models.ForeignKey(TrainDetails,on_delete=models.CASCADE)
	source=models.CharField(max_length=5)
	destination=models.CharField(max_length=5)
	totalPrice=models.IntegerField()

class PassengerDetails(models.Model):
	name=models.CharField(max_length=20)
	age=models.IntegerField()
	gender=models.CharField(max_length=5)
	coachNo=models.CharField(max_length=5)
	seatNo=models.IntegerField()
	PNRno=models.ForeignKey(BookedTicketDetails,on_delete=models.CASCADE)
		
class CoachDetails(models.Model):
	coachCC=models.IntegerField()
	coach2S=models.IntegerField()
	
class TimeTable(models.Model):
	trainNo=models.ForeignKey(TrainDetails,on_delete=models.CASCADE)
	stationID=models.ForeignKey(Station,on_delete=models.CASCADE)
	arrival=models.CharField(max_length=5)
	departure=models.CharField(max_length=5)
