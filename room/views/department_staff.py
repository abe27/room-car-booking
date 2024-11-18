from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from company_department.models import Department
from django.contrib import messages  # type: ignore
from django.http import JsonResponse


def index(request):
    context = {
        "url": "department_staff",
    }

    # เคลียร์ข้อความก่อนเข้าสู่หน้า
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # ลูปเพื่อเคลียร์ข้อความทั้งหมด

    if request.user.is_authenticated and request.user.is_staff:
        departments = Department.objects.filter(fccorp=request.user.fccorp)
        context.update(
            {
                "departments": departments,
            }
        )
        return render(request, "room/staff/department/index.html", context)
    else:
        return redirect("/")
    
def add_department(request):
    if request.method == "POST":
        fcname = request.POST.get("fcname", "").strip()
        if fcname:
            Department.objects.create(
                fcname=fcname, fccorp=request.user.fccorp
            )
            messages.success(request, "แผนกถูกเพิ่มเรียบร้อยแล้ว!")
        return redirect("department_staff")


def edit_department(request, pk):
    if request.method == "POST":
        department = get_object_or_404(Department, pk=pk, fccorp=request.user.fccorp)
        fcname = request.POST.get("fcname", "").strip()
        if fcname:
            department.fcname = fcname
            department.save()
            messages.success(request, "แก้ไขแผนกเรียบร้อยแล้ว!")
        return redirect("department_staff")


def delete_department(request, pk):
    if request.method == "POST":
        try:
            department = get_object_or_404(Department, pk=pk, fccorp=request.user.fccorp)
            department.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "เกิดข้อผิดพลาด"})
