from django import forms
from .models import Room
from company_department.models import Company


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
