from django.shortcuts import render
from django.http import JsonResponse
from company_department.models import Department
from user.models import Employee


# Create your views here.
def load_departments(request):
    fccorp_id = request.GET.get("fccorp")
    departments = Department.objects.filter(fccorp_id=fccorp_id).all()
    return JsonResponse(list(departments.values("id", "fcname")), safe=False)


def update_user_status(request):
    if (
        request.method == "POST"
        and request.user.is_authenticated
        and request.user.is_staff
    ):
        user_id = request.POST.get("user_id")
        is_active = request.POST.get("is_active") == "true"
        try:
            user = Employee.objects.get(id=user_id, fccorp=request.user.fccorp)
            user.is_active = is_active
            user.save()
            return JsonResponse(
                {"success": True, "message": "สถานะได้รับการอัปเดตเรียบร้อยแล้ว"}
            )
        except Employee.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "ไม่พบผู้ใช้งานที่ระบุ"}, status=404
            )
    return JsonResponse({"success": False, "message": "การร้องขอไม่ถูกต้อง"}, status=400)


def reset_password(request):
    if (
        request.method == "POST"
        and request.user.is_authenticated
        and request.user.is_staff
    ):
        user_id = request.POST.get("user_id")
        new_password = request.POST.get("new_password")

        if not new_password or len(new_password) < 8:
            return JsonResponse(
                {"success": False, "message": "รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร"}, status=400
            )

        try:
            user = Employee.objects.get(id=user_id, fccorp=request.user.fccorp)
            user.set_password(new_password)
            user.save()

            return JsonResponse({"success": True, "message": "รีเซ็ตรหัสผ่านสำเร็จ"})
        except Employee.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "ไม่พบผู้ใช้งานที่ระบุ"}, status=404
            )

    return JsonResponse({"success": False, "message": "การร้องขอไม่ถูกต้อง"}, status=400)
