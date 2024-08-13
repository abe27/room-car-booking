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
        "id",
        "room",
        "title",
        "description",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
        "status",
        "approver",
        "remark",
    ]
    list_filter = [
        "room",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
        "status",
    ]
    search_fields = ["id", "start_date", "end_date", "created_at", "title"]
    ordering = ["-start_date", "-end_date", "-created_at"]


# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Booking, BookingAdmin)
