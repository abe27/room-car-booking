from django.db import models
from company_department.models import Company
from user.models import Employee


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    detail = models.TextField(default="", blank=True)
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


class Status(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    color = models.CharField(max_length=255, default="", blank=True)
    sequence = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, related_name="bookings", blank=True, null=True
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="bookings_employee",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField(default="", blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        related_name="bookings",
        blank=True,
        null=True,
    )
    approver = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="bookings_approver",
        blank=True,
        null=True,
    )
    remark = models.CharField(max_length=255, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
