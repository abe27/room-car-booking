from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from room.models import Booking, Status


def confirm_booking(request, booking_id):
    context = {}
    if request.user.is_authenticated:
        user_id = request.user.id
        user_company = request.user.fccorp
        booking = Booking.objects.filter(
            room__company=user_company,
            employee__id=user_id,
            id=booking_id,
        ).first()

        if booking is None:
            context.update(
                {
                    "title": "เกิดข้อผิดพลาด",
                    "detail": "กรุณาเข้าสู่ระบบด้วยบัญชีที่ท่านได้ทำการจองห้องประชุม",
                    "image": "error",
                }
            )
        else:
            if booking.status.sequence == 1:
                status = get_object_or_404(Status, sequence=4)
                # ทำการยืนยันการเข้าห้องประชุม
                booking.status = status
                booking.save()
                context.update(
                    {
                        "title": "สำเร็จ",
                        "detail": "ยืนยันการเข้าห้องประชุมเสร็จสิ้น",
                        "image": "success",
                    }
                )
            else:
                context.update(
                    {
                        "title": "เกิดข้อผิดพลาด",
                        "detail": "ท่านเคยยืนยันการเข้าห้องประชุมนี้แล้ว",
                        "image": "error",
                    }
                )
        return render(request, "room/confirm_booking/index.html", context)
    else:
        return redirect("/")
