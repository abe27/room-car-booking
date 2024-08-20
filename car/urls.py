from django.urls import path, include
from car import views

urlpatterns = [
    path("", views.car, name="car"),
    path("profile", views.profile, name="car_profile"),
    path("booking/", views.booking, name="car_booking"),
    path("fetch_bookings/", views.fetch_bookings, name="car_fetch_bookings"),
    path("save_booking/", views.save_booking, name="car_save_booking"),
    path("cancel_booking/", views.cancel_booking, name="car_cancel_booking"),
    path("history/", views.history, name="car_history"),
    
    path(
        "approve-booking/<int:booking_id>/",
        views.approve_booking,
        name="car_approve_booking",
    ),
    path(
        "reject-booking/<int:booking_id>/",
        views.reject_bookings,
        name="car_reject_booking",
    ),
    path(
        "staff-cancel-booking/<int:booking_id>/",
        views.staff_cancel_bookings,
        name="car_staff-cancel-booking",
    ),
    
    path("approve/waiting/", views.waiting, name="car_waiting"),
    path("approve/approved/", views.approved, name="car_approved"),
    path("approve/rejected/", views.rejected, name="car_rejected"),
    path("approve/cancel/", views.cancel, name="car_cancel"),
    path("approve/all/", views.all_status, name="car_all_status"),
    path("approve/all_waiting/", views.all_waiting_bookings, name="car_all_waiting"),
    path("approve/all_approved/", views.all_approved_bookings, name="car_all_approved"),
    path("approve/all_rejected/", views.all_rejected_bookings, name="car_all_rejected"),
    path("approve/all_cancel/", views.all_cancel_bookings, name="car_all_cancel"),
    path("approve/all_all/", views.all_all_status_bookings, name="car_all_all_status"),
]
