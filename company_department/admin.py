from django.contrib import admin
from .models import Company, Department

class CompanyAdmin(admin.ModelAdmin) :
    list_display = ['fcskid', 'fcname', "image"]
    ordering = ['-fcname']
    
class DepartmentAdmin(admin.ModelAdmin) :
    list_display = ['fcskid', 'fcname', 'fccorp']
    list_filter = ['fccorp']
    ordering = ['-fccorp']
    
# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)