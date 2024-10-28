from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from room.models import Room, Booking
from datetime import datetime


def booking(request):
    context = {"url": "booking"}
    if request.user.is_authenticated:
        if request.method == "POST":
            date = request.POST.get("date")
            start_time = request.POST.get("start_time")
            end_time = request.POST.get("end_time")

            # Convert the input date and times to datetime objects
            start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

            # Query for rooms that are not booked during the specified time range
            booked_rooms = (
                # sequence 0 = Waiting, sequence 2 = Rejected, sequence 3 = Canceled
                Booking.objects.exclude(status__sequence__in=[0, 2, 3])
                .filter(start_date__lt=end_datetime, end_date__gt=start_datetime)
                .values_list("room_id", flat=True)
            )

            available_rooms = (
                Room.objects.filter(company=request.user.fccorp, status__name="Active")
                .exclude(id__in=booked_rooms)
                .order_by("sequence")
            )

            context.update(
                {
                    "date": date,
                    "start_time": start_time,
                    "end_time": end_time,
                    "rooms": available_rooms,
                }
            )

            return render(request, "room/booking/index.html", context)
        else:
            return render(request, "room/booking/index.html", context)
    else:
        return redirect("/")
