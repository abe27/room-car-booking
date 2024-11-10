from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from room.models import Room, Booking, Status
from datetime import datetime, timedelta
from django.contrib import messages  # type: ignore
from django.http import JsonResponse  # type: ignore
from django.utils.timezone import make_aware  # type: ignore


def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_company = request.user.fccorp
        # Get the start and end of today's date range
        today_start = make_aware(
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        )
        today_end = make_aware(
            datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        )
        bookings = Booking.objects.filter(
            room__company=user_company,
            employee__id=user_id,
            status__sequence__in=[1, 4, 5],
            start_date__range=(today_start, today_end),
            # sequence 1 = Approved, sequence 4 = Check-in, sequence 5 = Check-out
        )

        today = datetime.now()
        # เพิ่มเวลาปัจจุบันบวก 1 ชั่วโมง
        today_plus_one_hour = make_aware(today + timedelta(hours=1))
        context = {
            "bookings": bookings,
            "url": "checkin_checkout",
            "today": today_plus_one_hour,
        }
        return render(request, "room/checkin_checkout/index.html", context)
    else:
        return redirect("/")


def check_in(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)
        if booking.status.sequence == 1:
            booking.status = Status.objects.get(sequence=4)
            booking.check_in = datetime.now()
            booking.save()
            return JsonResponse({"success": True, "message": "Check-in successful!"})
        return JsonResponse(
            {"success": False, "message": "Booking is not approved yet."}
        )


def check_out(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)
        if booking.status.sequence == 4:  # Check-in
            booking.status = Status.objects.get(sequence=5)  # Check-out
            booking.check_out = datetime.now()
            booking.save()
            return JsonResponse({"success": True, "message": "Check-out successful!"})
        return JsonResponse(
            {"success": False, "message": "Booking has not been checked in yet."}
        )
