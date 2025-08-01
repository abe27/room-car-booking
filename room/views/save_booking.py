from django.http import JsonResponse  # type: ignore
from room.models import Room, Booking, Status
from datetime import datetime
import requests  # type: ignore

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
                status__sequence__in=[
                    1,
                    4,
                ],  # sequence 1 = Approved, sequence 4 = Confirmed
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

            # # Send Line Notify
            # line_notify_token = request.user.fccorp.line_notify_room
            # line_notify_url = "https://notify-api.line.me/api/notify"
            # headers = {"Authorization": f"Bearer {line_notify_token}"}

            # message = (
            #     f"\nBooking ID: {booking.id}\n"
            #     f"Room: {booking.room.name}\n"
            #     f"Title: {booking.title}\n"
            #     f"Requester: {booking.employee.first_name} {booking.employee.last_name}\n"
            #     f"Description: {booking.description}\n"
            #     f"Tel: {booking.employee.tel}\n"
            #     f"Start: {booking.start_date.strftime('%d/%m/%Y %H:%M')}\n"
            #     f"End: {booking.end_date.strftime('%d/%m/%Y %H:%M')}\n"
            #     f"Status: {booking.status.name}"
            # )
            # payload = {"message": message}

            # response = requests.post(line_notify_url, headers=headers, data=payload)
            # if response.status_code != 200:
            #     return JsonResponse(
            #         {"status": "Booking saved, but failed to send Line notification."},
            #         status=200,
            #     )
            # else:
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