from django.urls import path, include
from room import views

urlpatterns = [
    path("", views.room, name="room"),
    path("booking/", views.booking, name="booking"),
    path("fetch_bookings/", views.fetch_bookings, name="fetch_bookings"),
    path("save_booking/", views.save_booking, name="save_booking"),
    path("history/", views.history, name="history"),
    path("approve/waiting/", views.waiting, name="waiting"),
    path(
        "approve-booking/<int:booking_id>/",
        views.approve_booking,
        name="approve_booking",
    ),
    path("approve/approved/", views.approved, name="approved"),
    path("approve/rejected/", views.rejected, name="rejected"),
    path("approve/cancel/", views.cancel, name="cancel"),
    path("approve/all/", views.all_status, name="all_status"),
]
