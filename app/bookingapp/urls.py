from django.urls import path
from . import views

urlpatterns = [
    # default/landing page
    path('', views.homepage, name="homepage"),
    path('filter_flights/', views.filter_flights, name='filter_flights'),

    # login/profile related urls
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name="login"),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile/cancelbooking/<int:booking_id>/', views.cancelbooking, name='cancelbooking'),

    # flight related urls
    path('flightdetails/<int:flight_id>/', views.flightdetails, name='flightdetails'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('show-confirmation/<int:booking_id>/', views.show_confirmation, name='show_confirmation'),

    # these are the debug print paths
    path('debugplanes/', views.debugPlanes, name='debugplanes'),
    path('debugroutes/', views.debugRoutes, name='debugroutes'),
    path('debugflights/', views.debugFlights, name='debugflights'),
    path('debugpass/', views.debugpass, name='debugpass'),
    path('debugbooking/', views.debugBooking, name='debugbooking'),

    # these are the DELETE paths -> removes all related records
    path('delplanes/', views.delplanes, name='delplanes'),
    path('delflight/', views.delflight, name='delflights'),
    path('delbooking/', views.delbooking, name='delbooking'),
]
