from django.shortcuts import get_object_or_404  # type: ignore
from django.http import JsonResponse  # type: ignore
from room.models import  Booking, Status

def cancel_booking(request):
    if request.method == "POST":
        booking_id = request.POST.get("id")
        remark = request.POST.get("remark")  # รับค่าหมายเหตุจากคำขอ

        # ดึงข้อมูลการจองตาม booking_id และตรวจสอบว่าผู้ใช้เป็นเจ้าของ
        booking = get_object_or_404(Booking, id=booking_id, employee=request.user)

        # ตั้งสถานะเป็น "Canceled"
        booking.status = Status.objects.get(sequence=3)
        booking.remark = remark  # บันทึกหมายเหตุใน Booking
        booking.save()

        return JsonResponse({"success": True})

    return JsonResponse(
        {"success": False, "error": "Invalid request method"}, status=400
    )
