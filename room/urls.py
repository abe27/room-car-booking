from django.urls import path, include
from room import views

urlpatterns = [
    path("home", views.room, name="room"),
    path("fetch_bookings/", views.fetch_bookings, name="fetch_bookings"),
    path("save_booking/", views.save_booking, name="save_booking"),
]
