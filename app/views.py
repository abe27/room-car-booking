from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from company_department.models import Company, Department
from user.models import Employee
from django.contrib.auth.hashers import make_password


# Create your views here.
def sign_out(request):
    logout(request)
    return redirect("/")


def index(request):
    if request.user.is_authenticated:
        return render(request, "home/index.html")
    else:
        return redirect("signin")


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        return render(request, "accounts/signin/index.html")


def sign_up(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        emp_id = request.POST.get("emp_id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        fccorp_id = request.POST.get("fccorp_id")
        fcdept_id = request.POST.get("fcdept_id")

        if password == confirm_password:
            try:
                company = Company.objects.get(id=fccorp_id)
                department = Department.objects.get(id=fcdept_id)

                user = Employee.objects.create(
                    first_name=firstname,
                    last_name=lastname,
                    username=emp_id,
                    email=email,
                    password=make_password(password),
                    fccorp=company,
                    fcdept=department,
                )
                return redirect("signin")
            except Company.DoesNotExist:
                # Handle company not found error
                pass
            except Department.DoesNotExist:
                # Handle department not found error
                pass

    companies = Company.objects.all()
    departments = Department.objects.all()

    context = {
        "companies": companies,
        "departments": departments,
    }

    return render(request, "accounts/signup/index.html", context=context)
