from django.urls import path, include
from room import views

urlpatterns = [
    path("", views.room, name="room"),
    path("booking/", views.booking, name="booking"),
    path("fetch_bookings/", views.fetch_bookings, name="fetch_bookings"),
    path("save_booking/", views.save_booking, name="save_booking"),
    path('cancel_booking/', views.cancel_booking, name='cancel_booking'),
    path("history/", views.history, name="history"),

    path(
        "approve-booking/<int:booking_id>/",
        views.approve_booking,
        name="approve_booking",
    ),
    path(
        "reject-booking/<int:booking_id>/",
        views.reject_bookings,
        name="reject_booking",
    ),
    
    path("approve/waiting/", views.waiting, name="waiting"),
    path("approve/approved/", views.approved, name="approved"),
    path("approve/rejected/", views.rejected, name="rejected"),
    path("approve/cancel/", views.cancel, name="cancel"),
    path("approve/all/", views.all_status, name="all_status"),
    
    path("approve/all_waiting/", views.all_waiting_bookings, name="all_waiting"),
    path("approve/all_approved/", views.all_approved_bookings, name="all_approved"),
    path("approve/all_rejected/", views.all_rejected_bookings, name="all_rejected"),
    path("approve/all_cancel/", views.all_cancel_bookings, name="all_cancel"),
    path("approve/all_all/", views.all_all_status_bookings, name="all_all_status"),
]
