from django.shortcuts import render
from django.http import JsonResponse
from company_department.models import Department

# Create your views here.
def load_departments(request):
    fccorp_id = request.GET.get('fccorp')
    departments = Department.objects.filter(fccorp_id=fccorp_id).all()
    return JsonResponse(list(departments.values('id', 'fcname')), safe=False)
