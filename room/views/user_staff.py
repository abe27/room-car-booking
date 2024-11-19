from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from user.models import Employee
from django.contrib import messages  # type: ignore
from django.http import JsonResponse
from room.forms import UserForm


def index(request):
    context = {
        "url": "user_staff",
    }

    # เคลียร์ข้อความก่อนเข้าสู่หน้า
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # ลูปเพื่อเคลียร์ข้อความทั้งหมด

    if request.user.is_authenticated and request.user.is_staff:
        users = Employee.objects.filter(fccorp=request.user.fccorp)
        if request.method == "POST":
            form = UserForm(
                request.POST, user=request.user
            )  # ส่ง request.user ใน POST
            if form.is_valid():
                form.save()
                messages.success(request, "เพิ่มผู้ใช้สำเร็จ!")  # เพิ่มข้อความแจ้งเตือน
                return redirect("user_staff")
        else:
            form = UserForm(user=request.user)  # ส่ง request.user ใน GET
        context.update(
            {
                "users": users,
                "form": form
            }
        )
        return render(request, "room/staff/user/index.html", context)
    else:
        return redirect("/")

def update_status(request):
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
