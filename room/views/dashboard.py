from django.shortcuts import render, redirect  # type: ignore
from room.models import Room, Booking
import json


def dashboard(request):
    context = {"url": "dashboard"}
    if request.user.is_authenticated:
        rooms = Room.objects.filter(company=request.user.fccorp)
        context.update({"rooms": rooms})
        if request.method == "POST":
            room_id = request.POST.get("room_id")

            # Fetch selected room and bookings
            selectedRoom = Room.objects.get(id=room_id)
            bookings = Booking.objects.filter(
                room__id=room_id,
                status__sequence__in=[
                    1,
                    4,
                ],  # sequence 1 = Approved, sequence 4 = Confirmed
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
                    }
                )

            # Update context with selected room, its bookings, and serialized bookings data
            context.update(
                {
                    "bookings": json.dumps(
                        bookings_data
                    ),  # Ensure that bookings are JSON string
                    "selectedRoom": selectedRoom,
                }
            )
            return render(request, "room/dashboard/index.html", context)
        else:
            return render(request, "room/dashboard/index.html", context)
    else:
        return redirect("/")
