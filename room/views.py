from django.shortcuts import render
from django.http import JsonResponse
from .models import Room, Booking, Status
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_datetime


def room(request):
    user_company = request.user.fccorp
    rooms = Room.objects.filter(company=user_company)
    context = {
        "rooms": rooms,
        "default_room": rooms[0] if rooms.exists() else None,  # เพิ่ม default_room
    }
    return render(request, "room/home/index.html", context)


def booking(request):
    room_id = request.GET.get("room_id")
    rooms = Room.objects.filter(id=room_id)
    context = {
        "rooms": rooms,
    }
    return render(request, "room/booking/index.html", context)


def fetch_bookings(request):
    room_id = request.GET.get("room_id")
    # ดึง Status ที่มี sequence เท่ากับ 0 หรือ 1
    statuses = Status.objects.filter(sequence__in=[0, 1])
    bookings = Booking.objects.filter(room_id=room_id, status__in=statuses)
    booking_data = []
    for booking in bookings:
        booking_data.append(
            {
                "emp_id": booking.employee.emp_id,
                "first_name": booking.employee.first_name,
                "last_name": booking.employee.last_name,
                "title": booking.title,
                "start_date": booking.start_date.isoformat(),
                "end_date": booking.end_date.isoformat(),
                "description": booking.description,
                "status": booking.status.name,
                "color": booking.status.color,
            }
        )
    # print(booking_data)
    return JsonResponse({"bookings": json.dumps(booking_data)})


@csrf_exempt
def save_booking(request):
    if request.method == "POST":
        try:
            data = request.POST
            title = data.get("title")
            description = data.get("description")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            room_id = data.get("room_id")

            try:
                room = Room.objects.get(id=room_id)
            except Room.DoesNotExist:
                return JsonResponse(
                    {"status": "Room not found."},
                    status=404,
                )

            # Validate dates
            start_date_obj = parse_datetime(start_date)
            end_date_obj = parse_datetime(end_date)
            if start_date_obj == end_date_obj:
                print("Test")
                return JsonResponse(
                    {"status": "Start date and end date cannot be the same."},
                    status=400,
                )
            if end_date_obj < start_date_obj:
                return JsonResponse(
                    {"status": "End date cannot be earlier than start date."},
                    status=400,
                )

            employee = request.user
            status = Status.objects.get(sequence=0)

            Booking.objects.create(
                room=room,
                employee=employee,
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                status=status,
            )

            return JsonResponse({"status": "Booking saved successfully!"}, status=200)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse(
                {"status": f"An unexpected error occurred: {str(e)}"},
                status=500,
            )

    return JsonResponse({"status": "Invalid request"}, status=400)
