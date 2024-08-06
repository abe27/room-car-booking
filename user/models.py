from django.db import models
from django.contrib.auth.models import AbstractUser
from company_department.models import Company, Department

# Create your models here.
class Employee(AbstractUser):
    fccorp = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='companys', blank=True, null=True)
    fcdept = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='departments', blank=True, null=True)
    emp_id = models.CharField(max_length=10, default="", blank=True)
    
    def __str__(self) :
        return f"{self.username}"
