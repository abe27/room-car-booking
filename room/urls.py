from django.urls import path, include
from room import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="room_dashboard"),
    path("booking/", views.booking, name="room_booking"),
    path("profile", views.profile, name="profile"),
    path("save_booking/", views.save_booking, name="room_save_booking"),
    path("cancel_booking/", views.cancel_booking, name="room_cancel_booking"),
    path("history/", views.history, name="room_history"),
    path("approve/cancel/", views.cancel, name="room_cancel"),
]
