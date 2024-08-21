from django.contrib import admin
from .models import Car_Status, Car, Booking_Status, Booking, Location


class Car_Status_Admin(admin.ModelAdmin):
    list_display = ["id", "name"]


class CarAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "company", "image", "status", "sequence"]
    ordering = ["-sequence"]
    list_filter = [
        "company",
    ]


class Booking_Status_Admin(admin.ModelAdmin):
    list_display = ["id", "name", "color", "sequence"]
    ordering = ["-sequence"]


class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "car",
        "status",
        "company",
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
        "car",
        "company",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
        "status",
    ]
    search_fields = ["id", "start_date", "end_date", "created_at", "title"]
    ordering = ["-start_date", "-end_date", "-created_at"]


class LocationAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["-id"]


# Register your models here.
admin.site.register(Car_Status, Car_Status_Admin)
admin.site.register(Car, CarAdmin)
admin.site.register(Booking_Status, Booking_Status_Admin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Location, LocationAdmin)
