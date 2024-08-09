from django.contrib import admin
from .models import Room, Status, Booking


class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "company"]
    ordering = ["-name"]


class StatusAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "sequence"]
    ordering = ["-sequence"]


class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "start_date",
        "end_date",
        "status",
        "approver",
        "remark",
    ]
    ordering = ["-title"]


# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Booking, BookingAdmin)
