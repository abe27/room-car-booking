from django import forms
from .models import Room
from company_department.models import Company, Department
from user.models import Employee


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "detail", "remark", "sequence", "maximum_capacity", "status", "company", "image"]
        labels = {
            "name": "ชื่อห้อง",
            "detail": "รายละเอียด",
            "remark": "หมายเหตุ",
            "sequence": "ลำดับห้องประชุม",
            "maximum_capacity": "รองรับจำนวนผู้เข้าร่วมประชุม",
            "status": "สถานะ",
            "company": "บริษัท",
            "image": "ภาพห้องประชุม",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "detail": forms.Textarea(
                attrs={"class": "form-control", "required": True, "rows": 3}
            ),
            "remark": forms.Textarea(
                attrs={"class": "form-control", "required": True, "rows": 3}
            ),
            "sequence": forms.NumberInput(
                attrs={"class": "form-control", "required": True}
            ),
            "maximum_capacity": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "status": forms.Select(attrs={"class": "form-select", "required": True}),
            "company": forms.Select(attrs={"class": "form-select", "required": True}),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control", "required": True}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # รับค่า user ผ่าน kwargs
        super(RoomForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields["company"].queryset = Company.objects.filter(id=user.fccorp.id)

class UserForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["emp_id", "email", "username", "password", "first_name", "last_name", "tel", "fccorp", "fcdept"]
        labels = {
            "emp_id": "รหัสพนักงาน",
            "email": "อีเมล",
            "username": "ชื่อผู้ใช้",
            "password": "รหัสผ่าน",
            "first_name": "ชื่อจริง",
            "last_name": "นามสกุล",
            "tel": "เบอร์โทร",
            "fccorp": "บริษัท",
            "fcdept": "แผนก",
        }
        widgets = {
            "emp_id": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control", "required": True}),
            "username": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "required": True}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "tel": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "fccorp": forms.HiddenInput(attrs={"required": True}),
            "fcdept": forms.Select(attrs={"class": "form-select", "required": True}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # รับค่า user ผ่าน kwargs
        super(UserForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields["fccorp"].initial = user.fccorp.id if user.fccorp else "ไม่ระบุบริษัท"
            self.fields["fcdept"].queryset = Department.objects.filter(fccorp=user.fccorp)
            
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        # เข้ารหัสรหัสผ่านก่อนบันทึก
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
