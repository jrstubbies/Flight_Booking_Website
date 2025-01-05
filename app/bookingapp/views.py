from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from bookingapp.models import Passenger, Flight, Plane, Route, Booking
from datetime import datetime
from django.utils.dateformat import format as date_format
from django.http import JsonResponse


# deliver the homepage and some flights to be displayed (only first 40 flights shown)
def homepage(request):
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    # Order flights so most recent first, only show flights that haven't already departed
    flights = Flight.objects.order_by('depDate', 'depTime').filter(
        Q(depDate=current_date, depTime__gte=current_time) | Q(depDate__gt=current_date)
    )[:40]

    return render(request, 'homepage.html', {'flights': flights})


# Used for the filter functionality
def filter_flights(request):
    # store the value from the datepickers, and dropdowns
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    flights_query = Q()  # create an empty initial query

    # Only apply filters that were submitted
    if origin:
        flights_query &= Q(routeId__origin=origin)
    if destination:
        flights_query &= Q(routeId__destination=destination)

    # If given a start date then use this as the filter
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        flights_query &= Q(depDate__gte=start_date)

    # if NO start time given, then filter using the current date and time
    else:
        flights_query &= Q(depDate__gte=datetime.now().date(), depTime__gte=datetime.now().time()) | Q(depDate__gt=datetime.now().date())

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        flights_query &= Q(depDate__lte=end_date)

    # get flights based on the built up query filter, and order by most recent flights
    flights = Flight.objects.filter(flights_query).order_by('depDate', 'depTime')[:40]

    # Serialize flights data. Vhange the formatting for dates and times for easier reading
    flights_data = [{'flightId': f.flightId, 'origin': f.routeId.origin, 'destination': f.routeId.destination,
                     'depDate': date_format(f.depDate, 'F j, Y'),
                     'depTime': date_format(f.depTime, 'P'),
                     'arrDate': date_format(f.arrDate, 'F j, Y'),
                     'arrTime': date_format(f.arrTime, 'P'),
                     'route': {'planeId': {'code': f.routeId.planeId.code}}}
                    for f in flights]

    return JsonResponse(flights_data, safe=False)


# check for valid user if POST, if not valid then return page with error. If GET then send html
def login(request):
    # for TESTING PURPOSES, return users in database
    users = Passenger.objects.all()

    # if user tries login, check they are a valid user
    if request.method == 'POST':
        if 'submit' in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            try:
                # use a simple session value to flag if valid login or not
                user = Passenger.objects.get(username=username, password=password)
                request.session['user_id'] = user.passengerId
                request.session['is_logged_in'] = True
                return redirect('homepage')

            except Passenger.DoesNotExist:
                err_msg = "Invalid username or password."
                return render(request, 'login.html', {'error_message': err_msg, 'users': users})

        # if user clicks signup instead of login, then render signup page
        elif 'signup' in request.POST:
            return redirect('signup')

    # if NOT POST then send the login page
    return render(request, 'login.html', {'users': users})


# Deliver the signup/register page to create new user
def signup(request):
    # when the user submits data need to check that the username is not already taken
    if request.method == 'POST':
        username = request.POST['username']

        if Passenger.objects.filter(username=username).exists():
            err_msg = "Username already taken"
            return render(request, 'signup.html', {'error_message': err_msg})

        # if username is available create a new person and add to database
        else:
            p = Passenger(
                fName=request.POST['fname'],
                lName=request.POST['lname'],
                phone=int(request.POST['phone']),
                email=request.POST['email'],
                username=request.POST['username'],
                password=request.POST['password']
            )
            p.save()
            return redirect('login')

    # if NOT POST just return the signup page
    return render(request, 'signup.html', {})


# return a page for a particular flight to give more details and allow user to book
def flightdetails(request, flight_id):
    # check that the flight exists first, if not display error page
    try:
        # Find the amount of seats left on the flight. Return the view with this information
        flight = Flight.objects.get(flightId=flight_id)
        availseats = flight.seatsAvailable - Booking.objects.filter(flightId=flight_id).count()
        return render(request, 'flight_details.html', {'flight': flight, 'availseats': availseats})

    # if the flight doesnt exist then send the error page which will print the specific error
    except Flight.DoesNotExist:
        msg = "The flight you requested does not exist"
        return render(request, 'error.html', {'msg': msg})


# logout function
def logout(request):
    # simply delete the session value field to force the logout
    if 'is_logged_in' in request.session:
        del request.session['is_logged_in']
        del request.session['user_id']
    return redirect('homepage')


# Deals with creating the booking record only, calls other function to display html
def confirmation(request):
    if request.method == 'POST':

        # access the hidden value field of the form submit, and session value for user id
        flightid = request.POST.get('flight_id')
        userid = request.session['user_id']

        # if the flight exists then create the record, call another function to display information
        try:
            flight = Flight.objects.get(flightId=flightid)
            user = Passenger.objects.get(passengerId=userid)

            # create a new booking record to link the flight and passenger
            booking = Booking(
                userId=user,
                flightId=flight,
                whenBooked=datetime.now(),
            )
            booking.save()

            return redirect('show_confirmation', booking_id=booking.bookingId)

        # if flight or user doesnt exist render the error page with a message
        except Flight.DoesNotExist:
            msg = "404:   This flight does not exist"
            return render(request, 'confirmation.html', {'msg': msg})
        except Passenger.DoesNotExist:
            msg = "404:   User does not exist"
            return render(request, 'confirmation.html', {'msg': msg})


# Deals with the rendering of the page, prevents a refresh resubmitting the booking data
def show_confirmation(request, booking_id):
    # Retrieve the booking object based on the booking ID
    booking = Booking.objects.get(bookingId=booking_id)
    return render(request, 'confirmation.html', {'booking': booking})


# display the users profile page
def profile(request):
    try:
        # get the current user, and render html using their data
        userid = request.session['user_id']
        user = Passenger.objects.get(passengerId=userid)
        bookings = Booking.objects.filter(userId=userid)
        return render(request, 'profile.html', {'user': user, 'bookings': bookings})

    except Passenger.DoesNotExist:
        msg = "only a logged in user can view their profile"
        return render(request, 'error.html', {'msg': msg})


# If the user updates their details, deal with the POST
def update_profile(request):
    if request.method == 'POST':
        passenger_id = request.POST.get('passenger_id')
        passenger = Passenger.objects.get(passengerId=passenger_id)
        passenger.fName = request.POST.get('fName')
        passenger.lName = request.POST.get('lName')
        passenger.email = request.POST.get('email')
        passenger.phone = request.POST.get('phone')
        passenger.username = request.POST.get('username')
        passenger.password = request.POST.get('password')
        passenger.save()
        return redirect('profile')  # Redirect to the profile page after successful update

    return render(request, 'profile.html', {'user': request.user})


# if a user cancels a booking, then delete the record
def cancelbooking(request, booking_id):
    try:
        booking = Booking.objects.get(bookingId=booking_id)
        booking.delete()

    except Booking.DoesNotExist:
        msg = "this booking does not exist"
        return render(request, 'error.html', {'msg': msg})

    return redirect('profile')  # Redirect to the profile page after cancellation


# ----------------------------------------   DEBUG PRINTING RECORDS  -----------------------------------------
def debugPlanes(request):
    entries = Plane.objects.all()
    res = "displaying plane records" + '<br>'
    for entry in entries:
        res += '<br>' + entry.name + ' ' + '' + entry.code + ' ' + str(entry.numSeats)
    return HttpResponse(res)


def debugRoutes(request):
    entries = Route.objects.all()
    res = "displaying route records" + '<br>'
    for entry in entries:
        res += '<br>' + entry.routeName + ' ' + entry.origin + ' ' + entry.destination + ' ' + str(entry.planeId)
    return HttpResponse(res)


def debugFlights(request):
    entries = Flight.objects.all()
    res = "displaying flight records" + '<br>'
    for entry in entries:
        res += '<br>' + entry.routeId.routeName + ' ' + str(entry.depTime) + ' ' + str(entry.depDate) + ' ' + str(entry.arrTime) + ' ' + str(entry.arrDate) + ' ' + str(entry.seatsAvailable) + ' ' + str(entry.ticketCost)
    return HttpResponse(res)


def debugpass(request):
    entries = Passenger.objects.all()
    res = "displaying passenger records" + '<br>'
    for e in entries:
        res += '<br>' + e.fName + ' ' + e.lName + ' ' + e.username + ' ' + e.password
    return HttpResponse(res)


def debugBooking(request):
    entries = Booking.objects.all()
    res = "displaying booking records" + '<br>'
    for e in entries:
        res += '<br>' + str(e.bookingId) + ' ' + str(e.userId) + ' ' + str(e.flightId) + ' ' + str(e.whenBooked)
    return HttpResponse(res)


# ----------------------------------------   DELETE RECORDS  -----------------------------------------
def delplanes(request):
    entries = Plane.objects.all()
    for entry in entries:
        entry.delete()

    entries = Route.objects.all()
    for entry in entries:
        entry.delete()


def delflight(request):
    entries = Flight.objects.all()
    for e in entries:
        e.delete()


def delbooking(request):
    entries = Booking.objects.all()
    for e in entries:
        e.delete()
