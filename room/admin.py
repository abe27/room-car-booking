from django.contrib import admin
from .models import Room_Status, Room, Status, Booking


class Room_StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "company", "image", "status", "sequence"]
    ordering = ["-sequence"]
    list_filter = [
        "company",
    ]


class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "color", "sequence"]
    ordering = ["-sequence"]


class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room",
        "status",
        "title",
        "description",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
        "employee",
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
    ordering = ["-id"]


# Register your models here.
admin.site.register(Room_Status, Room_StatusAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Booking, BookingAdmin)
