from django.urls import path, include
from room import views

urlpatterns = [
    path("home", views.room, name="room"),
]
