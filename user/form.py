from django import forms
from .models import Employee
from company_department.models import Department

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fcdept'].queryset = Department.objects.none()

        if 'fccorp' in self.data:
            try:
                fccorp_id = int(self.data.get('fccorp'))
                self.fields['fcdept'].queryset = Department.objects.filter(fccorp_id=fccorp_id).order_by('fcname')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk and self.instance.fccorp:
            self.fields['fcdept'].queryset = Department.objects.filter(fccorp_id=self.instance.fccorp.id).order_by('fcname')
