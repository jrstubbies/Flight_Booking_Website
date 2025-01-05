# Flight_Booking_Website

A simple flight booking website built using Python and Django. The site 
allows users to view and filter upcoming flights, book a flight, manage previously
booked flights etc.

To run the webserver:

    1 - run the 'requirements.txt' file to ensure you have all the Python modules required. Run using:
            pip install -r "requirements.txt"

    2 - run the 'add_data.py' file to populate the database (may take couple of seconds depending on PC). 
        This data is just random passengers, planes, times etc so modify this data as needed. Run using:
            python add_data.py

    3 - start the server by running:
            python manage.py runserver

    4 - open any web browser and enter the URL (presuming running on same machine as server. Change the 
        port number as needed):
            localhost:8000/bookingapp

    5 - website is now up and running to play around with