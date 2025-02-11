from room.models import Room, Booking
from company_department.models import Company
from django.shortcuts import render, get_object_or_404
import json
from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone


def index(request):
    companies = Company.objects.all()
    company_id = request.GET.get("company")
    context = {}

    if company_id:
        rooms = Room.objects.filter(company_id=company_id)
        bookings = Booking.objects.filter(
            employee__fccorp_id=company_id,
            status__sequence__in=[1, 4, 5],
        )
        # print(list(bookings))
        bookings_data = []
        for booking in bookings:
            bookings_data.append(
                {
                    "id": booking.pk,
                    "emp_id": booking.employee.emp_id,
                    "first_name": booking.employee.first_name,
                    "last_name": booking.employee.last_name,
                    "title": booking.title,
                    "start_date": booking.start_date.isoformat(),
                    "end_date": booking.end_date.isoformat(),
                    "description": booking.description.replace("\r\n", "<br>").replace(
                        "\n", "<br>"
                    ),  # แปลง \r\n และ \n เป็น <br>
                    "status": booking.status.name,
                    "color": booking.status.color,
                    "remark": booking.remark.replace("\r\n", "<br>").replace(
                        "\n", "<br>"
                    ),  # แปลง \r\n และ \n เป็น <br>,
                }
            )

        context = {"bookings": json.dumps(bookings_data)}
    else:
        rooms = ""

    context.update(
        {
            "companies": companies,
            "rooms": rooms,
        }
    )
    return render(request, "room/calendar/index.html", context)


def detail(request, id):
    today = timezone.now().date()  # Get today's date
    room = get_object_or_404(Room, id=id)
    current_booking = (
        Booking.objects.filter(
            room=id,
            status__sequence__in=[1, 4],
            start_date__date=today,  # Filter bookings starting today
        )
        .order_by("start_date", "end_date")
        .first()
    )

    bookings = Booking.objects.filter(
        room=id,
        status__sequence__in=[1, 4, 5],
    )
    # print(list(bookings))
    bookings_data = []
    for booking in bookings:
        bookings_data.append(
            {
                "id": booking.pk,
                "emp_id": booking.employee.emp_id,
                "first_name": booking.employee.first_name,
                "last_name": booking.employee.last_name,
                "title": booking.title,
                "start_date": booking.start_date.isoformat(),
                "end_date": booking.end_date.isoformat(),
                "description": booking.description.replace("\r\n", "<br>").replace(
                    "\n", "<br>"
                ),  # แปลง \r\n และ \n เป็น <br>
                "status": booking.status.name,
                "color": booking.status.color,
                "remark": booking.remark.replace("\r\n", "<br>").replace(
                    "\n", "<br>"
                ),  # แปลง \r\n และ \n เป็น <br>,
            }
        )
    context = {
        "room": room,
        "current_booking": current_booking,
        "bookings": json.dumps(bookings_data),
    }
    return render(request, "room/calendar/detail.html", context)


def check_booking_update(request):
    """
    ตรวจสอบว่ามีการเปลี่ยนแปลงใน Booking หรือไม่
    """
    if cache.get("booking_updated"):
        cache.delete("booking_updated")  # ลบค่า cache หลังแจ้งเตือน
        return JsonResponse({"updated": True})  # แจ้งว่า booking มีการเปลี่ยนแปลง
    return JsonResponse({"updated": False})  # ไม่มีการเปลี่ยนแปลง
