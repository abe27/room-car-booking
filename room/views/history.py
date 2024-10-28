from django.shortcuts import render, redirect # type: ignore
from room.models import Room, Booking, Status
from datetime import datetime
from django.contrib import messages # type: ignore

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
        bookings = Booking.objects.filter(room__company=user_company)
        statuses = Status.objects.all().order_by("sequence")
        rooms = Room.objects.filter(company=request.user.fccorp).order_by("sequence")

        context = {
            "bookings": bookings,
            "url": "history_staff",
            "statuses": statuses,
            "rooms": rooms,
        }
        return render(request, "room/staff/history/index.html", context)
    else:
        return redirect("/")