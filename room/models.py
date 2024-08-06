from django.db import models
from company_department.models import Company
from user.models import Employee


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    image = models.CharField(max_length=255, default="", blank=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        related_name="rooms",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"


class Color(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, related_name="bookings", blank=True, null=True
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="bookings"
    )
    title = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField(default="", blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    flag = models.CharField(max_length=255, default="", blank=True)
    color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, related_name="bookings", blank=True, null=True
    )

    def __str__(self):
        return f"{self.title}"
