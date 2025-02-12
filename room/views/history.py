from django.shortcuts import render, redirect  # type: ignore
from room.models import Room, Booking, Status
from datetime import datetime, time
from django.contrib import messages  # type: ignore
from django.utils.dateparse import parse_date


def history(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_company = request.user.fccorp
        bookings = Booking.objects.filter(
            room__company=user_company, employee__id=user_id
        )
        statuses = Status.objects.all().order_by("sequence")
        rooms = Room.objects.filter(company=request.user.fccorp).order_by("sequence")
        # Check if the start date is in the past
        today = datetime.now()

        context = {
            "bookings": bookings,
            "url": "history",
            "statuses": statuses,
            "rooms": rooms,
            "today": today,
        }
        return render(request, "room/history/index.html", context)
    else:
        return redirect("/")


def history_staff(request):
    # เคลียร์ข้อความก่อนเข้าสู่หน้า
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # ลูปเพื่อเคลียร์ข้อความทั้งหมด

    if request.user.is_authenticated and request.user.is_staff:
        user_company = request.user.fccorp
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        bookings = Booking.objects.none()  # เริ่มต้นเป็น QuerySet ว่าง

        # ดึงข้อมูลเฉพาะเมื่อมี start_date หรือ end_date
        if start_date or end_date:
            bookings = Booking.objects.filter(room__company=user_company)

            if start_date:
                start_date = parse_date(start_date)
                bookings = bookings.filter(start_date__gte=start_date)

            if end_date:
                end_date = parse_date(end_date)
                end_date_format = datetime.combine(end_date, time.max)  # ตั้งเวลาเป็น 23:59:59
                bookings = bookings.filter(start_date__lte=end_date_format)

        statuses = Status.objects.all().order_by("sequence")
        rooms = Room.objects.filter(company=user_company).order_by("sequence")

        context = {
            "bookings": bookings,
            "url": "history_staff",
            "statuses": statuses,
            "rooms": rooms,
            "start_date": start_date.strftime("%Y-%m-%d") if start_date else "",
            "end_date": end_date.strftime("%Y-%m-%d") if end_date else "",
        }
        return render(request, "room/staff/history/index.html", context)
    else:
        return redirect("/")
