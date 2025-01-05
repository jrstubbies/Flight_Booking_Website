import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asn2.settings')
django.setup()

from datetime import datetime, timedelta
from bookingapp.models import Flight, Route, Passenger, Plane
from pytz import timezone


# create 3 months of flights for dairy flat to/from sydney
def sydneyFlights():
    schedules = [  # 0 = Mon ....   5 = Sat
        {'type': 'outbound', 'dep_day': 4, 'dep_time': '10:35'},
        {'type': 'inbound', 'dep_day': 6, 'dep_time': '14:30'},
    ]

    # get todays date and find the date for the mon of this week. Set the timezone values required
    today = datetime.now().date()
    this_monday = today - timedelta(days=today.weekday())
    syd_time = timezone('Australia/Sydney')
    nz_time = timezone('Pacific/Auckland')

    for week in range(20):
        # get the new/next weeks date for the monday by adding 7 days
        current_date = this_monday + timedelta(days=7 * week)

        # for inbound and outbound flight
        for schedule in schedules:

            # to the monday of the current week, add on the value for the day in the array
            weekday_date = current_date + timedelta(days=schedule['dep_day'])

            if schedule['type'] == 'outbound':
                route = Route.objects.get(routeName="DF-SYD")
                flight_duration = timedelta(hours=3, minutes=45)
                cost = 480.00
                origin_time = nz_time
                dest_time = syd_time
            else:
                route = Route.objects.get(routeName="SYD-DF")
                flight_duration = timedelta(hours=3)
                cost = 520.00
                origin_time = syd_time
                dest_time = nz_time

            # convert the times into the respective timezones
            dep_datetime = datetime.combine(weekday_date, datetime.strptime(schedule['dep_time'], "%H:%M").time())
            dep_datetime = dep_datetime.astimezone(origin_time)
            arr_datetime = dep_datetime + flight_duration
            arr_datetime = arr_datetime.astimezone(dest_time)

            new_flight = Flight(
                routeId=route,
                depTime=dep_datetime.time(),
                depDate=dep_datetime.date(),
                arrTime=arr_datetime.time(),
                arrDate=arr_datetime.date(),
                seatsAvailable=route.planeId.numSeats,
                ticketCost=cost
            )
            new_flight.save()


# Create 3 months of intial flights to Rotorua   -> will add flights starting from Mon of current days week
def rotoruaFlights():
    # Define the schedules for each type of flight
    schedules = [
        {'type': 'outbound_am', 'dep_time': '08:00'},
        {'type': 'outbound_pm', 'dep_time': '16:30'},
        {'type': 'inbound_am', 'dep_time': '09:30'},
        {'type': 'inbound_pm', 'dep_time': '18:00'},
    ]
    flight_duration = timedelta(minutes=45)

    # Get today's date. Find the Mon for the week of 'today'
    today = datetime.now().date()
    this_monday = today - timedelta(days=today.weekday())  # weekday is 0-6 for mon-sun. subtract off will give Mon date

    for week in range(20):
        # Calculate the start date for the current week
        current_date = this_monday + timedelta(days=7 * week)

        # Add flights only for weekdays (Monday to Friday)
        for day in range(5):  # 0 for Monday, 1 for Tuesday, ..., 4 for Friday
            weekday_date = current_date + timedelta(days=day)

            for schedule in schedules:
                # Calculate departure and arrival datetime for the current date and schedule
                dep_datetime = datetime.combine(weekday_date, datetime.strptime(schedule['dep_time'], "%H:%M").time())
                arr_datetime = dep_datetime + flight_duration

                # Determine the route based on the schedule type
                if 'outbound' in schedule['type']:
                    route = Route.objects.get(routeName='DF-ROT')
                    cost = 185.00
                else:
                    route = Route.objects.get(routeName='ROT-DF')
                    cost = 205.00

                # Create a new Flight instance and save it to the database
                new_flight = Flight(
                    routeId=route,
                    depTime=dep_datetime.time(),
                    depDate=weekday_date,
                    arrTime=arr_datetime.time(),
                    arrDate=weekday_date,
                    seatsAvailable=route.planeId.numSeats,
                    ticketCost=cost
                )
                new_flight.save()


# create 3 months of flighs to great barrier islad
def greatbarrierFlights():
    schedules = [  # 0 = Mon ....   5 = Sat
        {'type': 'outbound', 'dep_days': [0, 2, 4], 'dep_time': '09:30'},
        {'type': 'inbound', 'dep_days': [1, 3, 5], 'dep_time': '10:00'},
    ]
    flight_duration = timedelta(minutes=30)

    # get todays date and find the date for the mon of this week
    today = datetime.now().date()
    this_monday = today - timedelta(days=today.weekday())

    for week in range(20):
        # get the new/next weeks date for the monday by adding 7 days
        current_date = this_monday + timedelta(days=7 * week)

        # for inbound and outbound flight
        for schedule in schedules:

            # loop through the inbound/outbound days array to create a flight for each day
            for day in schedule['dep_days']:
                # to the monday of the current week, add on the value for the day in the array
                weekday_date = current_date + timedelta(days=day)

                dep_datetime = datetime.combine(weekday_date, datetime.strptime(schedule['dep_time'], "%H:%M").time())
                arr_datetime = dep_datetime + flight_duration

                if schedule['type'] == 'outbound':
                    route = Route.objects.get(routeName="DF-GBI")
                    cost = 190.00
                else:
                    route = Route.objects.get(routeName="GBI-DF")
                    cost = 210.00

                new_flight = Flight(
                    routeId=route,
                    depTime=dep_datetime.time(),
                    depDate=dep_datetime.date(),
                    arrTime=arr_datetime.time(),
                    arrDate=arr_datetime.date(),
                    seatsAvailable=route.planeId.numSeats,
                    ticketCost=cost
                )
                new_flight.save()


# add 3 months of flights to/from chatham island
def chathamFlights():
    schedules = [  # 0 = Mon ....   5 = Sat
        {'type': 'outbound', 'dep_days': [1, 4], 'dep_time': '11:30'},
        {'type': 'inbound', 'dep_days': [2, 5], 'dep_time': '10:45'},
    ]

    # get todays date and find the date for the mon of this week
    today = datetime.now().date()
    this_monday = today - timedelta(days=today.weekday())
    chat_time = timezone('Pacific/Chatham')
    nz_time = timezone('Pacific/Auckland')

    for week in range(20):
        # get the new/next weeks date for the monday by adding 7 days
        current_date = this_monday + timedelta(days=7 * week)

        # for inbound and outbound flight
        for schedule in schedules:

            # loop through the inbound/outbound days array to create a flight for each day
            for day in schedule['dep_days']:
                # to the monday of the current week, add on the value for the day in the array
                weekday_date = current_date + timedelta(days=day)

                if schedule['type'] == 'outbound':
                    route = Route.objects.get(routeName="DF-CHI")
                    flight_duration = timedelta(hours=2, minutes=15)
                    cost = 435.00
                    origin_time = nz_time
                    dest_time = chat_time
                else:
                    route = Route.objects.get(routeName="CHI-DF")
                    flight_duration = timedelta(hours=2, minutes=45)
                    cost = 500.00
                    origin_time = chat_time
                    dest_time = nz_time

                dep_datetime = datetime.combine(weekday_date, datetime.strptime(schedule['dep_time'], "%H:%M").time())
                dep_datetime = dep_datetime.astimezone(origin_time)
                arr_datetime = dep_datetime + flight_duration
                arr_datetime = arr_datetime.astimezone(dest_time)

                new_flight = Flight(
                    routeId=route,
                    depTime=dep_datetime.time(),
                    depDate=dep_datetime.date(),
                    arrTime=arr_datetime.time(),
                    arrDate=arr_datetime.date(),
                    seatsAvailable=route.planeId.numSeats,
                    ticketCost=cost
                )
                new_flight.save()


# add 3months of flights to lake tekapo
def tekapoFlights():
    schedules = [  # 0 = Mon ....   5 = Sat
        {'type': 'outbound', 'dep_day': 0, 'dep_time': '09:15'},
        {'type': 'inbound', 'dep_day': 1, 'dep_time': '17:25'},
    ]
    flight_duration = timedelta(hours=2, minutes=25)
    # get todays date and find the date for the mon of this week
    today = datetime.now().date()
    this_monday = today - timedelta(days=today.weekday())

    for week in range(20):
        # get the new/next weeks date for the monday by adding 7 days
        current_date = this_monday + timedelta(days=7 * week)

        # for inbound and outbound flight
        for schedule in schedules:

            # to the monday of the current week, add on the value for the day in the array
            weekday_date = current_date + timedelta(days=schedule['dep_day'])

            if schedule['type'] == 'outbound':
                route = Route.objects.get(routeName="DF-LKT")
                cost = 430.00
            else:
                route = Route.objects.get(routeName="LKT-DF")
                cost = 475.00

            dep_datetime = datetime.combine(weekday_date, datetime.strptime(schedule['dep_time'], "%H:%M").time())
            arr_datetime = dep_datetime + flight_duration

            new_flight = Flight(
                routeId=route,
                depTime=dep_datetime.time(),
                depDate=dep_datetime.date(),
                arrTime=arr_datetime.time(),
                arrDate=arr_datetime.date(),
                seatsAvailable=route.planeId.numSeats,
                ticketCost=cost
            )
            new_flight.save()



# function to add pre-determined passengers/users
def add_passengers():
    # remove any existing passengers
    entries = Passenger.objects.all()
    for entry in entries:
        entry.delete()

    # create 10 users for the database to keep it simple
    # For simplicity username is first name, password is last name
    user1 = Passenger(
        fName="Ella",
        lName="Lee",
        email="ella.lee@blobmail.com",
        phone=6308524916,
        username="ella",
        password="lee"
    )
    user1.save()

    user2 = Passenger(
        fName="Lucy",
        lName="Lopez",
        email="lucy.lopez@xyz.com",
        phone=1490782361,
        username="lucy",
        password="lopez"
    )
    user2.save()

    user3 = Passenger(
        fName="Noah",
        lName="Brown",
        email="noah.brown@yippee.com",
        phone=6001287842,
        username="noah",
        password="brown"
    )
    user3.save()

    user4 = Passenger(
        fName="Rick",
        lName="Cooper",
        email="rick.cooper@yippee.com",
        phone=2765840260,
        username="rick",
        password="cooper"
    )
    user4.save()

    user5 = Passenger(
        fName="Kevin",
        lName="Fields",
        email="kevin.fields@yippee.com",
        phone=1906152887,
        username="kevin",
        password="fields"
    )
    user5.save()


    user6 = Passenger(
        fName="Hema",
        lName="Naik",
        email="hema.naik@bazooka.com",
        phone=2857064302,
        username="hema",
        password="naik"
    )
    user6.save()


    user7 = Passenger(
        fName="Aatu",
        lName="Jarvi",
        email="aatu.jarvi@bazooka.com",
        phone=6256005586,
        username="aatu",
        password="jarvi"
    )
    user7.save()


    user8 = Passenger(
        fName="Sophie",
        lName="Lee",
        email="sophie.lee@blobmail.com",
        phone=7356144587,
        username="sophie",
        password="lee"
    )
    user8.save()


    user9 = Passenger(
        fName="Ruby",
        lName="Harper",
        email="ruby.harper@xyz.com",
        phone=5621052638,
        username="ruby",
        password="harper"
    )
    user9.save()

    user10 = Passenger(
        fName="Milo",
        lName="Martin",
        email="milo.martin@xyz.com",
        phone=5018162961,
        username="milo",
        password="martin"
    )
    user10.save()


# function to add planes and routes
def add_planes_routes():
    
    # delete the entries in plane and route tables
    entries = Plane.objects.all()
    for entry in entries:
        entry.delete()

    entries = Route.objects.all()
    for entry in entries:
        entry.delete()


    # Create the plane and routes for sydney
    syber = Plane(
        name="SyberJet",
        code="SJ30i",
        numSeats=6
    )
    syber.save()

    tosyd = Route(
        routeName="DF-SYD",
        origin="Dairy Flat (NZNE)",
        destination="Sydney (YSSY)",
        planeId=syber
    )
    tosyd.save()

    fromsyd = Route(
        routeName="SYD-DF",
        origin="Sydney (YSSY)",
        destination="Dairy Flat (NZNE)",
        planeId=syber
    )
    fromsyd.save()


    # create the first Cirrus plane, and give it the route of rotorua
    cira = Plane(
        name="Cirrus",
        code="SF50a",
        numSeats=4
    )
    cira.save()

    torot = Route(
        routeName="DF-ROT",
        origin="Dairy Flat (NZNE)",
        destination="Rotorua (NZRO)",
        planeId=cira
    )
    torot.save()

    fromrot = Route(
        routeName="ROT-DF",
        origin="Rotorua (NZRO)",
        destination="Dairy Flat (NZNE)",
        planeId=cira
    )
    fromrot.save()


    # Use the other cirrus plane for great barrier island
    cirb = Plane(
        name="Cirrus",
        code="SF50b",
        numSeats=4
    )
    cirb.save()

    togb = Route(
        routeName="DF-GBI",
        origin="Dairy Flat (NZNE)",
        destination="Great Barrier Island (NZGB)",
        planeId=cirb
    )
    togb.save()

    fromgb = Route(
        routeName="GBI-DF",
        origin="Great Barrier Island (NZGB)",
        destination="Dairy Flat (NZNE)",
        planeId=cirb
    )
    fromgb.save()


    # create first honda jetm with route to chatham island
    hona = Plane(
        name="HondaJet Elite",
        code="HJ70a",
        numSeats=5
    )
    hona.save()


    toci = Route(
        routeName="DF-CHI",
        origin="Dairy Flat (NZNE)",
        destination="Chatham Island (NZCI)",
        planeId=hona
    )
    toci.save()

    fromci = Route(
        routeName="CHI-DF",
        origin="Chatham Island (NZCI)",
        destination="Dairy Flat (NZNE)",
        planeId=hona
    )
    fromci.save()


    # create other honda jet, with route to lake tekapo
    honb = Plane(
        name="HondaJet Elite",
        code="HJ70b",
        numSeats=5
    )
    honb.save()

    tolt = Route(
        routeName="DF-LKT",
        origin="Dairy Flat (NZNE)",
        destination="Lake Tekapo (NZTL)",
        planeId=honb
    )
    tolt.save()

    fromlt = Route(
        routeName="LKT-DF",
        origin="Lake Tekapo (NZTL)",
        destination="Dairy Flat (NZNE)",
        planeId=honb
    )
    fromlt.save()

if __name__ == "__main__":

    # add the passengers
    add_passengers()
    
    # add the planes and routes
    add_planes_routes()
    
    # clear all the flight data first, then add new data
    entries = Flight.objects.all()
    for entry in entries:
        entry.delete()
       
    # add flights to the flight database
    rotoruaFlights()
    sydneyFlights()
    greatbarrierFlights()
    chathamFlights()
    tekapoFlights()

