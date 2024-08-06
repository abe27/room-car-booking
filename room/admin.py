from django.contrib import admin
from .models import Room, Color, Booking


class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "company"]
    ordering = ["-name"]


class ColorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ["-name"]


class BookingAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "start_date", "end_date", "flag"]
    ordering = ["-title"]


# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Booking, BookingAdmin)
