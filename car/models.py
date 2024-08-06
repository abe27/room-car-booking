from django.db import models

# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=100, default="", blank=True)
    image = models.CharField(max_length=100, default="", blank=True)
    def __str__(self) :
        return f"{self.name}"
