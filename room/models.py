from django.db import models
from company_department.models import Company
from user.models import Employee
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


# Create your models here.


class Room_Status(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return f"{self.name}"


class Room(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    detail = models.TextField(default="", blank=True)
    maximum_capacity = models.IntegerField(default=0, blank=True)
    image = models.ImageField(upload_to="room/images/", default="", blank=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        related_name="rooms",
        blank=True,
        null=True,
    )
    remark = models.TextField(default="", blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(
        Room_Status,
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
    remark = models.TextField(default="", blank=True)
    message = models.IntegerField(default=0, null=True, blank=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

@receiver(post_save, sender=Booking)
@receiver(post_delete, sender=Booking)
def booking_updated(sender, instance, **kwargs):
    print("Booking updated event")
    """
    เมื่อมีการสร้าง แก้ไข หรือ ลบ booking ให้ตั้งค่า cache 
    เพื่อใช้ตรวจสอบว่ามีการเปลี่ยนแปลงเกิดขึ้น
    """
    cache.set("booking_updated", True, timeout=120)  # ตั้งค่า cache ไว้ 120 วินาที