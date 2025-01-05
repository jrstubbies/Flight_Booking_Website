from django.db import models


# Table for information about a plane
class Plane(models.Model):
    planeId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False)
    code = models.CharField(max_length=10, null=False)
    numSeats = models.IntegerField(null=False)

    class Meta:
        db_table = 'plane'


# Table for information on a passenger
# 'unique=True' is used to ensure usernames and emails are all different
# 'blank=False' is used to ensure fields in forms require input
# 'null=False' is used to ensure that no NULL values can be stored in the database
class Passenger(models.Model):
    passengerId = models.AutoField(primary_key=True)
    fName = models.CharField(max_length=30, blank=False, null=False)
    lName = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.IntegerField(blank=False, null=False)
    username = models.CharField(max_length=20, unique=True, blank=False, null=False)
    password = models.CharField(max_length=20, blank=False, null=False)

    class Meta:
        db_table = 'passenger'


# Table for information about a route
class Route(models.Model):
    routeId = models.AutoField(primary_key=True)
    routeName = models.CharField(max_length=50, null=False)
    origin = models.CharField(max_length=50, null=False)
    destination = models.CharField(max_length=50, null=False)
    planeId = models.ForeignKey(Plane, related_name="routes", on_delete=models.CASCADE)

    class Meta:
        db_table = 'route'


# Table for a flights information
class Flight(models.Model):
    flightId = models.AutoField(primary_key=True)
    routeId = models.ForeignKey(Route, related_name="flights", on_delete=models.CASCADE)
    depTime = models.TimeField(null=False)        # hours, mins, secs
    depDate = models.DateField(null=False)        # default is yyyy-mm-dd
    arrTime = models.TimeField(null=False)
    arrDate = models.DateField(null=False)
    seatsAvailable = models.IntegerField(null=False)  # depends on the plane
    ticketCost = models.DecimalField(null=False, max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'flight'


# Junction table to connect passengers and their flight
class Booking(models.Model):
    bookingId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(Passenger, related_name="bookings", on_delete=models.CASCADE)
    flightId = models.ForeignKey(Flight, related_name="bookings", on_delete=models.CASCADE)
    whenBooked = models.DateTimeField()     # information for when the flight was booked

    class Meta:
        db_table = 'booking'
