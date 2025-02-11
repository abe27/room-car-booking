from django.shortcuts import render, redirect  # type: ignore
from room.models import Room, Booking
import json


def dashboard(request):
    context = {"url": "dashboard"}
    if request.user.is_authenticated:
        rooms = Room.objects.filter(company=request.user.fccorp)
        room_capacities = [
            {
                "id": 1,
                "name": "จำนวนผู้เข้าร่วมประชุม 1-5 คน",
                "start_capacity": 1,
                "end_capacity": 5,
            },
            {
                "id": 2,
                "name": "จำนวนผู้เข้าร่วมประชุม 6-10 คน",
                "start_capacity": 6,
                "end_capacity": 10,
            },
            {
                "id": 3,
                "name": "จำนวนผู้เข้าร่วมประชุม 11-20 คน",
                "start_capacity": 11,
                "end_capacity": 20,
            },
            {
                "id": 4,
                "name": "จำนวนผู้เข้าร่วมประชุม 20 คนขึ้นไป",
                "start_capacity": 21,
                "end_capacity": None,
            },
        ]

        context.update(
            {
                "rooms": rooms,
                "room_capacities": room_capacities,
            }
        )

        if request.method == "POST":
            capacity = request.POST.get("capacity")
            room_id = request.POST.get("room_id")

            # Fetch selected room and bookings
            selectedRoom = Room.objects.get(id=room_id)
            selectedCapacity = room_capacities[int(capacity) - 1]
            
            bookings = Booking.objects.filter(
                room__id=room_id,
                status__sequence__in=[
                    1,
                    4,
                    5,
                ],  # sequence 1 = Approved, sequence 4 = Check-in, sequence 5 = Check-out
            )

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
                        "description": booking.description.replace(
                            "\r\n", "<br>"
                        ).replace(
                            "\n", "<br>"
                        ),  # แปลง \r\n และ \n เป็น <br>
                        "status": booking.status.name,
                        "color": booking.status.color,
                        "remark": booking.remark.replace("\r\n", "<br>").replace(
                            "\n", "<br>"
                        ),  # แปลง \r\n และ \n เป็น <br>,
                        "room": booking.room.name
                    }
                )

            # Update context with selected room, its bookings, and serialized bookings data
            context.update(
                {
                    "bookings": json.dumps(
                        bookings_data
                    ),  # Ensure that bookings are JSON string
                    "selectedRoom": selectedRoom,
                    "selectedCapacity": selectedCapacity,
                }
            )
            return render(request, "room/dashboard/index.html", context)
        else:
            return render(request, "room/dashboard/index.html", context)
    else:
        return redirect("/")
