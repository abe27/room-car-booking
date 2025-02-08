from room.models import Booking, Room
from company_department.models import Company
from django.shortcuts import render, redirect
from django.utils import timezone


def list(request):
    if request.user.is_authenticated:
        today = timezone.now().date()  # Get today's date
        bookings = Booking.objects.filter(
            room__company=request.user.fccorp,
            status__sequence__in=[1, 4],
            start_date__date__gte=today,  # Filter bookings starting today or later
            # start_date__date=today  # Filter bookings starting today
        ).order_by("start_date")[:15]
        context = {"bookings": bookings}
        return render(request, "room/room/list/index.html", context)
    else:
        return redirect("/")


# def card(request):
#     if request.user.is_authenticated:
#         today = timezone.now().date()  # Get today's date
#         bookings = (
#             Booking.objects.filter(
#                 room__company=request.user.fccorp,
#                 status__sequence__in=[1, 4],
#                 start_date__date=today,  # Filter bookings starting today
#             )
#             .order_by("start_date", "end_date")[:15]
#         )
#         context = {"bookings": bookings}
#         return render(request, "room/room/card/index.html", context)
#     else:
#         return redirect("/")


def company(request):
    companies = Company.objects.all()
    context = {"companies": companies}
    return render(request, "room/company/index.html", context)


def card(request, id):
    today = timezone.now().date()
    rooms = Room.objects.filter(company=id)

    # ดึงรายการจองของวันนี้
    bookings = Booking.objects.filter(
        room__company=id,
        status__sequence__in=[1, 4],
        start_date__date=today,
    ).order_by("start_date", "end_date")

    # สร้าง mapping ระหว่างห้องกับการจอง
    room_booking_map = {booking.room.id: booking for booking in bookings}

    # สร้าง list ของการ์ดห้อง
    room_cards = []
    for room in rooms:
        if room.id in room_booking_map:
            room_cards.append({"room": room, "booking": room_booking_map[room.id]})
        else:
            room_cards.append({"room": room, "booking": None})  # ห้องที่ไม่มีการจอง

    # แปลง timezone ของ datetime.max ให้เป็น offset-aware
    max_dt = timezone.make_aware(timezone.datetime.max)

    # เรียงลำดับตาม start_date (ห้องที่ไม่มีการจองอยู่ท้ายสุด)
    sorted_bookings = sorted(
        room_cards,
        key=lambda x: (
            x["booking"].start_date if x["booking"] else max_dt,
            x["booking"].end_date if x["booking"] else max_dt,
        ),
    )

    context = {
        "room_cards": sorted_bookings,
    }
    return render(request, "room/room/card/index.html", context)
