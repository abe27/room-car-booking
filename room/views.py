from django.shortcuts import render
from django.http import JsonResponse
from .models import Room, Booking
from django.views.decorators.csrf import csrf_exempt
import json


def room(request):
    user_company = request.user.fccorp
    rooms = Room.objects.filter(company=user_company)
    bookings = Booking.objects.filter(room__company=user_company)

    # Convert datetime fields to string format
    booking_data = []
    for booking in bookings:
        booking_data.append(
            {
                "title": booking.title,
                "start_date": booking.start_date.isoformat(),  # Convert datetime to ISO format
                "end_date": booking.end_date.isoformat(),  # Convert datetime to ISO format
                "description": booking.description,
            }
        )

    context = {
        "rooms": rooms,
        "bookings": json.dumps(booking_data),
    }
    return render(request, "room/index.html", context)


def fetch_bookings(request):
    room_id = request.GET.get("room_id")
    # print("room id: ", room_id)
    bookings = Booking.objects.filter(room_id=room_id)
    booking_data = []
    for booking in bookings:
        booking_data.append(
            {
                "title": booking.title,
                "start_date": booking.start_date.isoformat(),
                "end_date": booking.end_date.isoformat(),
                "description": booking.description,
            }
        )
    # print(booking_data)
    return JsonResponse({"bookings": json.dumps(booking_data)})


@csrf_exempt
def save_booking(request):
    if request.method == "POST":
        data = request.POST
        title = data.get("title")
        description = data.get("description")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        room_id = data.get("room_id")

        room = Room.objects.get(id=room_id)
        employee = request.user

        Booking.objects.create(
            room=room,
            employee=employee,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )

        return JsonResponse({"status": "Booking saved successfully!"})
    return JsonResponse({"status": "Invalid request"}, status=400)
