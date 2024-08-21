from django.db import models
from company_department.models import Company
from user.models import Employee


# Create your models here.
class Car_Status(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return f"{self.name}"


class Car(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    detail = models.TextField(default="", blank=True)
    image = models.ImageField(upload_to="car/images/", default="", blank=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        related_name="cars",
        blank=True,
        null=True,
    )
    car_year = models.CharField(max_length=255, default="", blank=True)
    car_registration = models.CharField(max_length=255, default="", blank=True)
    remark = models.TextField(default="", blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(
        Car_Status,
        on_delete=models.SET_NULL,
        related_name="cars",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"


class Booking_Status(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    color = models.CharField(max_length=255, default="", blank=True)
    sequence = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.name}"


class Location(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        related_name="car_bookings",
        blank=True,
        null=True,
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="car_bookings_employee",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255, default="", blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name="car_bookings",
        blank=True,
        null=True,
    )
    description = models.TextField(default="", blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.ForeignKey(
        Booking_Status,
        on_delete=models.SET_NULL,
        related_name="car_bookings",
        blank=True,
        null=True,
    )
    approver = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="car_bookings_approver",
        blank=True,
        null=True,
    )
    remark = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
