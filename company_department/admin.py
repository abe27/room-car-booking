from django.contrib import admin
from .models import Company, Department


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["fcname", "image", "id"]
    ordering = ["-id"]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["fcname", "fccorp", "id"]
    list_filter = ["fccorp"]
    ordering = ["-fccorp"]


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
