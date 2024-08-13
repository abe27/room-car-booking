from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee
from .form import EmployeeForm


class EmployeeAdmin(UserAdmin):
    form = EmployeeForm  # ใช้ฟอร์มที่เราสร้างขึ้น

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "emp_id", "email")}),
        (
            "Additional info",
            {
                "fields": (
                    "fccorp",
                    "fcdept",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    def display_groups(self, obj):
        return ", ".join(group.name for group in obj.groups.all())

    display_groups.short_description = "Groups"

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "display_groups",
        "fccorp",
        "fcdept",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    class Media:
        js = ("user/js/filterDept.js",)


admin.site.register(Employee, EmployeeAdmin)
