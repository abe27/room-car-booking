from django.urls import path, include
from room import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="room_dashboard"),
    path("booking/", views.booking, name="room_booking"),
    path("save_booking/", views.save_booking, name="room_save_booking"),
    path("cancel_booking/", views.cancel_booking, name="room_cancel_booking"),
    path("history/", views.history, name="room_history"),
    path("history/staff/", views.history_staff, name="room_history_staff"),
    path("edit/booking/", views.edit_booking, name="edit_booking"),
    path("room/staff/", views.room_staff, name="room_staff"),
    path("edit/room/", views.edit_room, name="edit_room"),
    path("delete-room/", views.delete_room, name="delete_room"),
    path(
        "confirm_booking/<int:booking_id>",
        views.confirm_booking,
        name="confirm_booking",
    ),
]
