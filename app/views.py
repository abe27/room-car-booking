from django.http import JsonResponse # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from company_department.models import Company, Department
from user.models import Employee
from django.contrib.auth.hashers import make_password # type: ignore
from room.models import Room
from car.models import Car


# Create your views here.
def sign_out(request):
    logout(request)
    return redirect("/")


def index(request):
    if request.user.is_authenticated:
        return render(request, "app/home/index.html")
    else:
        return redirect("signin")


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Invalid username or password. If your account is inactive, please contact the administrator.",
                    }
                )

        return render(request, "app/accounts/signin/index.html")


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            emp_id = request.POST.get("emp_id")
            username = request.POST.get("username")
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
                        emp_id=emp_id,
                        username=username,
                        email=email,
                        password=make_password(password),
                        fccorp=company,
                        fcdept=department,
                        is_active=False,
                    )
                    return JsonResponse({"success": True, "redirect_url": "/signin"})
                except Company.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "error": "Company not found"}
                    )
                except Department.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "error": "Department not found"}
                    )
                except Exception as e:
                    return JsonResponse({"success": False, "error": str(e)})
            else:
                return JsonResponse(
                    {"success": False, "error": "Passwords do not match"}
                )

        companies = Company.objects.all()
        departments = Department.objects.all()

        context = {
            "companies": companies,
            "departments": departments,
        }

        return render(request, "app/accounts/signup/index.html", context=context)
