from django.http import JsonResponse  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth import authenticate, login, logout  # type: ignore
from company_department.models import Company, Department
from user.models import Employee
from django.contrib.auth.hashers import make_password  # type: ignore


# Create your views here.
def sign_out(request):
    logout(request)
    return redirect("/")


def index(request):
    if request.user.is_authenticated:
        return render(request, "app/index/index.html")
    else:
        return redirect("home")


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username_or_email = request.POST.get("username_or_email")
            password = request.POST.get("password")

            # First try to authenticate by username
            user = authenticate(request, username=username_or_email, password=password)

            # If authentication fails, try to authenticate by email
            if user is None:
                try:
                    # Find user by email
                    user = Employee.objects.get(email=username_or_email)
                    user = authenticate(
                        request, username=user.username, password=password
                    )
                except Employee.DoesNotExist:
                    user = None

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
            # username = request.POST.get("username")
            username = f"{firstname.lower()}.{lastname[:3].lower()}"
            email = request.POST.get("email")
            tel = request.POST.get("tel")
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
                        tel=tel,
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


def profile(request):
    if request.user.is_authenticated:
        return render(request, "app/accounts/profile/index.html")
    else:
        return redirect("/")

def home(request):
    return render(request, "app/home/index.html")