from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from django.http import JsonResponse  # type: ignore
from room.models import Room_Status, Room
from django.contrib import messages  # type: ignore
from company_department.models import Company
from room.forms import RoomForm


def room_staff(request):
    context = {
        "url": "room_staff",
    }

    # เคลียร์ข้อความก่อนเข้าสู่หน้า
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # ลูปเพื่อเคลียร์ข้อความทั้งหมด

    if request.user.is_authenticated and request.user.is_staff:
        rooms = Room.objects.filter(company=request.user.fccorp).order_by("sequence")
        statuses = Room_Status.objects.all()
        companies = Company.objects.filter(id=request.user.fccorp.id)

        if request.method == "POST":
            form = RoomForm(
                request.POST, request.FILES, user=request.user
            )  # ส่ง request.user ใน POST
            if form.is_valid():
                form.save()
                messages.success(request, "เพิ่มห้องประชุมสำเร็จ!")  # เพิ่มข้อความแจ้งเตือน
                return redirect("room_staff")
        else:
            form = RoomForm(user=request.user)  # ส่ง request.user ใน GET

        context.update(
            {"rooms": rooms, "statuses": statuses, "form": form, "companies": companies}
        )
        return render(request, "room/staff/room/index.html", context)
    else:
        return redirect("/")


def edit_room(request):
    if request.method == "POST":
        room_id = request.POST.get("id")
        room = get_object_or_404(Room, id=room_id)

        # อัปเดตข้อมูลทั่วไป
        room.name = request.POST.get("name")
        room.detail = request.POST.get("detail")
        room.remark = request.POST.get("remark")
        room.sequence = request.POST.get("sequence")
        room.status_id = request.POST.get("status")
        room.company_id = request.POST.get("company")

        # ตรวจสอบว่ามีการอัปโหลดภาพใหม่หรือไม่
        if "image" in request.FILES and request.FILES["image"]:
            room.image = request.FILES["image"]

        room.save()
        messages.success(request, "อัพเดทห้องประชุมสำเร็จ!")  # เพิ่มข้อความแจ้งเตือน

        return redirect("room_staff")


def delete_room(request):
    if (
        request.method == "POST"
        and request.user.is_authenticated
        and request.user.is_staff
    ):
        room_id = request.POST.get("id")
        try:
            room = Room.objects.get(id=room_id, company=request.user.fccorp)
            room.delete()
            return JsonResponse({"success": True})
        except Room.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "ห้องประชุมไม่พบหรือไม่มีสิทธิ์ในการลบ"}
            )
    return JsonResponse({"success": False, "message": "คำขอลบไม่ถูกต้อง"})
