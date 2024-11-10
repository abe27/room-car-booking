from django.urls import path, include
from room import views

urlpatterns = [
    path("dashboard/", views.dashboard.dashboard, name="room_dashboard"),
    path("booking/", views.booking.booking, name="room_booking"),
    path("save_booking/", views.save_booking.save_booking, name="room_save_booking"),
    path("cancel_booking/", views.cancel_booking.cancel_booking, name="room_cancel_booking"),
    path("history/", views.history.history, name="room_history"),
    path("history/staff/", views.history.history_staff, name="room_history_staff"),
    path("edit/booking/", views.edit_booking.edit_booking, name="edit_booking"),
    path("room/staff/", views.room_staff.room_staff, name="room_staff"),
    path("edit/room/", views.room_staff.edit_room, name="edit_room"),
    path("delete-room/", views.room_staff.delete_room, name="delete_room"),
    path(
        "confirm_booking/<int:booking_id>",
        views.confirm_booking.confirm_booking,
        name="confirm_booking",
    ),
    path("checkin_checkout/", views.checkin_checkout.index, name="checkin_checkout"),
    path("check_in/<int:booking_id>/", views.checkin_checkout.check_in, name="room_check_in"),
    path("check_out/<int:booking_id>/", views.checkin_checkout.check_out, name="room_check_out"),
]
