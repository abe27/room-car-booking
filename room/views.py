from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from django.http import JsonResponse  # type: ignore
from .models import Room_Status, Room, Booking, Status
import json
from datetime import datetime
import requests  # type: ignore


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
            booked_rooms = Booking.objects.filter(
                start_date__lt=end_datetime, end_date__gt=start_datetime
            ).values_list("room_id", flat=True)

            available_rooms = (
                Room.objects.filter(company=request.user.fccorp)
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


def dashboard(request):
    context = {"url": "dashboard"}
    if request.user.is_authenticated:
        rooms = Room.objects.filter(company=request.user.fccorp)
        context.update({"rooms": rooms})
        if request.method == "POST":
            room_id = request.POST.get("room_id")

            # Fetch selected room and bookings
            selectedRoom = Room.objects.get(id=room_id)
            bookings = Booking.objects.filter(room__id=room_id)

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
                        "description": booking.description,
                        "status": booking.status.name,
                        "color": booking.status.color,
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


def save_booking(request):
    if request.method == "POST":
        try:
            data = request.POST
            title = data.get("title")
            description = data.get("description")
            date = data.get("date")
            start_time = data.get("start_time")
            end_time = data.get("end_time")
            room_id = data.get("room_id")

            try:
                room = Room.objects.get(id=room_id)
            except Room.DoesNotExist:
                return JsonResponse(
                    {"status": "Room not found."},
                    status=404,
                )

            if start_time > end_time:
                return JsonResponse(
                    {"status": "Start time cannot be later than end time."},
                    status=400,
                )
            # Convert the input date and times to datetime objects
            start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

            # Check if the start date is in the past
            today = datetime.now().date()
            start_date = start_datetime.date()
            if start_date < today:
                return JsonResponse(
                    {"status": "Cannot book a room for a past date."},
                    status=400,
                )

            if start_datetime == end_datetime:
                return JsonResponse(
                    {"status": "Start date and end date cannot be the same."},
                    status=400,
                )

            # Check if there are any bookings with status sequence 1 during the requested time period
            conflicting_bookings = Booking.objects.filter(
                room=room,
                status__name="Approved",
                start_date__lt=end_datetime,
                end_date__gt=start_datetime,
            )
            if conflicting_bookings.exists():
                return JsonResponse(
                    {"status": "The selected time slot is not available."},
                    status=400,
                )

            employee = request.user
            status = Status.objects.get(sequence=1)  # sequence 1 is Approved

            # Save the booking
            booking = Booking.objects.create(
                room=room,
                employee=employee,
                title=title,
                description=description,
                start_date=start_datetime,
                end_date=end_datetime,
                status=status,
            )

            # Send Line Notify
            line_notify_token = request.user.fccorp.line_notify_room
            line_notify_url = "https://notify-api.line.me/api/notify"
            headers = {"Authorization": f"Bearer {line_notify_token}"}

            message = (
                f"\nBooking ID: {booking.id}\n"
                f"Room: {booking.room.name}\n"
                f"Title: {booking.title}\n"
                f"Requester: {booking.employee.first_name} {booking.employee.last_name}\n"
                f"Description: {booking.description}\n"
                f"Tel: {booking.employee.tel}\n"
                f"Start: {booking.start_date.strftime('%d/%m/%Y %H:%M')}\n"
                f"End: {booking.end_date.strftime('%d/%m/%Y %H:%M')}\n"
                f"Status: {booking.status.name}"
            )
            payload = {"message": message}

            response = requests.post(line_notify_url, headers=headers, data=payload)
            if response.status_code != 200:
                return JsonResponse(
                    {"status": "Booking saved, but failed to send Line notification."},
                    status=200,
                )
            else:
                return JsonResponse(
                    {
                        "status": "Booking saved and Line notification sent successfully!"
                    },
                    status=200,
                )

        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse(
                {"status": f"An unexpected error occurred: {str(e)}"},
                status=500,
            )

    return JsonResponse({"status": "Invalid request"}, status=400)


def cancel_booking(request):
    booking_id = request.POST.get("id")
    booking = get_object_or_404(Booking, id=booking_id, employee=request.user)
    booking.status = Status.objects.get(name="Canceled")
    booking.save()

    return JsonResponse({"success": True})


def history(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_company = request.user.fccorp
        bookings = Booking.objects.filter(
            room__company=user_company, employee__id=user_id
        ).order_by("-created_at")
        statuses = Status.objects.all().order_by("sequence")
        context = {
            "bookings": bookings,
            "url": "history",
            "statuses": statuses,
        }
        return render(request, "room/history/index.html", context)
    else:
        return redirect("/")


def profile(request):
    if request.user.is_authenticated:
        room_id = request.GET.get("room_id")
        room = Room.objects.filter(id=room_id).first()
        context = {"room": room, "url": "profile"}
        return render(request, "room/profile/index.html", context)
    else:
        return redirect("/")


def cancel(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(
                room__company=user_company, room=room, status__name="Canceled"
            ).order_by("-created_at")
            context = {"room": room, "bookings": bookings, "url": "cancel"}
            return render(request, "room/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")
