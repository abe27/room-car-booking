from django.urls import path, include
from room import views

urlpatterns = [
    path("", views.room, name="room"),
    path("profile", views.profile, name="profile"),
    path("booking/", views.booking, name="room_booking"),
    path("fetch_bookings/", views.fetch_bookings, name="room_fetch_bookings"),
    path("save_booking/", views.save_booking, name="room_save_booking"),
    path("cancel_booking/", views.cancel_booking, name="room_cancel_booking"),
    path("history/", views.history, name="room_history"),
    
    path(
        "approve-booking/<int:booking_id>/",
        views.approve_booking,
        name="room_approve_booking",
    ),
    path(
        "reject-booking/<int:booking_id>/",
        views.reject_bookings,
        name="room_reject_booking",
    ),
    path(
        "staff-cancel-booking/<int:booking_id>/",
        views.staff_cancel_bookings,
        name="room_staff-cancel-booking",
    ),
    
    path("approve/waiting/", views.waiting, name="room_waiting"),
    path("approve/approved/", views.approved, name="room_approved"),
    path("approve/rejected/", views.rejected, name="room_rejected"),
    path("approve/cancel/", views.cancel, name="room_cancel"),
    path("approve/all/", views.all_status, name="room_all_status"),
    path("approve/all_waiting/", views.all_waiting_bookings, name="room_all_waiting"),
    path("approve/all_approved/", views.all_approved_bookings, name="room_all_approved"),
    path("approve/all_rejected/", views.all_rejected_bookings, name="room_all_rejected"),
    path("approve/all_cancel/", views.all_cancel_bookings, name="room_all_cancel"),
    path("approve/all_all/", views.all_all_status_bookings, name="room_all_all_status"),
]
