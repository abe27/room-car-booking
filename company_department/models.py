from django.db import models


# Create your models here.
class Company(models.Model):
    fcskid = models.CharField(max_length=10, default="", blank=True, unique=True)
    fcname = models.CharField(max_length=100, default="", blank=True)
    image = models.ImageField(upload_to="company/images/", default="", blank=True)
    line_notify_room = models.CharField(
        max_length=255, default="", blank=True, null=True
    )
    line_notify_car = models.CharField(
        max_length=255, default="", blank=True, null=True
    )

    def __str__(self):
        return f"{self.fcname}"


class Department(models.Model):
    fcskid = models.CharField(max_length=10, default="", blank=True, unique=True)
    fcname = models.CharField(max_length=100, default="", blank=True)
    fccorp = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="departments"
    )

    def __str__(self):
        return f"{self.fcname}"
