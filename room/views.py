from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from django.http import JsonResponse  # type: ignore
from .models import Room_Status, Room, Booking, Status
from django.views.decorators.csrf import csrf_exempt  # type: ignore
import json
from datetime import datetime
import requests  # type: ignore


def profile(request):
    if request.user.is_authenticated:
        room_id = request.GET.get("room_id")
        room = Room.objects.filter(id=room_id).first()
        context = {"room": room, "url": "profile"}
        return render(request, "room/profile/index.html", context)
    else:
        return redirect("/")


def room(request):
    if request.user.is_authenticated:
        user_company = request.user.fccorp
        room_status = Room_Status.objects.get(name="Active")
        rooms = Room.objects.filter(company=user_company, status=room_status).order_by(
            "sequence"
        )
        context = {
            "rooms": rooms,
            "default_room": rooms[0] if rooms.exists() else None,  # เพิ่ม default_room
        }
        return render(request, "room/home/index.html", context)
    else:
        return redirect("/")


def booking(request):
    if request.user.is_authenticated:
        room_id = request.GET.get("room_id")
        room = Room.objects.filter(id=room_id).first()
        context = {"room": room, "url": "booking"}
        return render(request, "room/booking/index.html", context)
    else:
        return redirect("/")


def fetch_bookings(request):
    room_id = request.GET.get("room_id")
    statuses = Status.objects.filter(name__in=["Waiting", "Approved"])
    bookings = Booking.objects.filter(room_id=room_id, status__in=statuses)
    booking_data = []
    for booking in bookings:
        booking_data.append(
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
    # print(booking_data)
    return JsonResponse({"bookings": json.dumps(booking_data)})


# @csrf_exempt
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
            # Convert start_date to ISO format
            # end_date_obj = parse_datetime(end_date)
            try:
                start_date_obj = datetime.strptime(start_date, "%d/%m/%Y %H:%M")
                start_date_iso = start_date_obj.isoformat()
            except ValueError:
                return JsonResponse(
                    {"status": "Invalid start date format."},
                    status=400,
                )

            try:
                end_date_obj = datetime.strptime(end_date, "%d/%m/%Y %H:%M")
                end_date_iso = end_date_obj.isoformat()
            except ValueError:
                return JsonResponse(
                    {"status": "Invalid end date format."},
                    status=400,
                )

            if start_date_obj == end_date_obj:
                return JsonResponse(
                    {"status": "Start date and end date cannot be the same."},
                    status=400,
                )
            if end_date_obj < start_date_obj:
                return JsonResponse(
                    {"status": "End date cannot be earlier than start date."},
                    status=400,
                )

            # Check if there are any bookings with status sequence 1 during the requested time period
            conflicting_bookings = Booking.objects.filter(
                room=room,
                status__name="Approved",
                start_date__lt=end_date_obj,
                end_date__gt=start_date_obj,
            )
            if conflicting_bookings.exists():
                return JsonResponse(
                    {"status": "The selected time slot is not available."},
                    status=400,
                )

            employee = request.user
            status = Status.objects.get(name="Waiting")

            # Save the booking
            booking = Booking.objects.create(
                room=room,
                employee=employee,
                title=title,
                description=description,
                start_date=start_date_iso,
                end_date=end_date_iso,
                status=status,
            )

            # Send Line Notify
            line_notify_token = request.user.fccorp.line_notify_room
            line_notify_url = "https://notify-api.line.me/api/notify"
            headers = {"Authorization": f"Bearer {line_notify_token}"}
            message = f"\nBooking ID: {booking.id}\nRoom: {booking.room.name}\nTitle: {booking.title}\nRequester: {booking.employee.first_name} {booking.employee.last_name}\nDescription: {booking.description}\nTel: {booking.employee.tel}\nStart: {booking.start_date}\nEnd: {booking.end_date}\nStatus: {booking.status.name}"
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
        room_id = request.GET.get("room_id")
        room = Room.objects.filter(id=room_id).first()
        bookings = Booking.objects.filter(
            room__company=user_company, employee__id=user_id
        ).order_by("-created_at")
        context = {"room": room, "bookings": bookings, "url": "history"}
        return render(request, "room/history/index.html", context)
    else:
        return redirect("/")


def waiting(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(
                room__company=user_company, room=room, status__name="Waiting"
            ).order_by("created_at")
            context = {"room": room, "bookings": bookings, "url": "waiting"}
            return render(request, "room/waiting/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def approved(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(
                room__company=user_company, room=room, status__name="Approved"
            ).order_by("-created_at")
            context = {"room": room, "bookings": bookings, "url": "approved"}
            return render(request, "room/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def rejected(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(
                room__company=user_company, room=room, status__name="Rejected"
            ).order_by("-created_at")
            context = {"room": room, "bookings": bookings, "url": "rejected"}
            return render(request, "room/approve/index.html", context)
        else:
            return redirect("/")
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


def all_status(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(
                room__company=user_company, room=room
            ).order_by("-created_at")
            context = {"room": room, "bookings": bookings, "url": "all_status"}
            return render(request, "room/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def approve_booking(request, booking_id):
    # booking = Booking.objects.get(id=booking_id)
    booking = get_object_or_404(Booking, id=booking_id)

    # Set the status to Approved
    approved_status = get_object_or_404(Status, name="Approved")
    booking.status = approved_status

    # Assign the approver as the current logged-in user
    booking.approver = request.user

    # Parse the JSON body to get the remark
    data = json.loads(request.body)
    remark = data.get("remark", "").strip()

    booking.remark = remark
    booking.save()

    # Reject other bookings that overlap with the approved booking
    overlapping_bookings = Booking.objects.filter(
        room=booking.room,
        status__name="Waiting",
        start_date__lt=booking.end_date,
        end_date__gt=booking.start_date,
    ).exclude(id=booking.id)

    rejected_status = get_object_or_404(Status, name="Rejected")

    for other_booking in overlapping_bookings:
        other_booking.status = rejected_status
        other_booking.approver = request.user
        other_booking.remark = "มีคนจองห้องนี้แล้ว"
        other_booking.save()

    # Send Line Notify
    line_notify_token = request.user.fccorp.line_notify_room
    line_notify_url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {line_notify_token}"}
    message = f"\nBooking ID: {booking.id}\nRoom: {booking.room.name}\nTitle: {booking.title}\nRequester: {booking.employee.first_name} {booking.employee.last_name}\nDescription: {booking.description}\nTel: {booking.employee.tel}\nStart: {booking.start_date}\nEnd: {booking.end_date}\nRemark: {booking.remark}\nStatus: {booking.status.name}"
    payload = {"message": message}

    response = requests.post(line_notify_url, headers=headers, data=payload)
    if response.status_code != 200:
        return JsonResponse(
            {
                "status": "Booking approved successfully!, but failed to send Line notification."
            },
            status=200,
        )
    else:
        return JsonResponse(
            {
                "status": "Booking approved successfully and Line notification sent successfully!"
            },
            status=200,
        )


def reject_bookings(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)

        # Get the status for Rejected
        rejected_status = get_object_or_404(Status, name="Rejected")
        booking.status = rejected_status

        # Assign the approver as the current logged-in user
        booking.approver = request.user

        # Parse the JSON body to get the remark
        data = json.loads(request.body)
        remark = data.get("remark", "").strip()

        if not remark:
            return JsonResponse({"status": "Remark cannot be empty!"}, status=400)

        booking.remark = remark
        booking.save()

        # Send Line Notify
        line_notify_token = request.user.fccorp.line_notify_room
        line_notify_url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        message = f"\nBooking ID: {booking.id}\nRoom: {booking.room.name}\nTitle: {booking.title}\nRequester: {booking.employee.first_name} {booking.employee.last_name}\nDescription: {booking.description}\nTel: {booking.employee.tel}\nStart: {booking.start_date}\nEnd: {booking.end_date}\nRemark: {booking.remark}\nStatus: {booking.status.name}"
        payload = {"message": message}

        response = requests.post(line_notify_url, headers=headers, data=payload)
        if response.status_code != 200:
            return JsonResponse(
                {
                    "status": "Booking rejected successfully!, but failed to send Line notification."
                },
                status=200,
            )
        else:
            return JsonResponse(
                {
                    "status": "Booking rejected successfully and Line notification sent successfully!"
                },
                status=200,
            )

    return JsonResponse({"status": "Invalid request method."}, status=405)


def staff_cancel_bookings(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)

        # Get the status for Rejected
        canceled_status = get_object_or_404(Status, name="Canceled")
        booking.status = canceled_status

        # Assign the approver as the current logged-in user
        booking.approver = request.user

        # Parse the JSON body to get the remark
        data = json.loads(request.body)
        remark = data.get("remark", "").strip()

        if not remark:
            return JsonResponse({"status": "Remark cannot be empty!"}, status=400)

        booking.remark = remark
        booking.save()
        # Send Line Notify
        line_notify_token = request.user.fccorp.line_notify_room
        line_notify_url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        message = f"\nBooking ID: {booking.id}\nRoom: {booking.room.name}\nTitle: {booking.title}\nRequester: {booking.employee.first_name} {booking.employee.last_name}\nDescription: {booking.description}\nTel: {booking.employee.tel}\nStart: {booking.start_date}\nEnd: {booking.end_date}\nRemark: {booking.remark}\nStatus: {booking.status.name}"
        payload = {"message": message}

        response = requests.post(line_notify_url, headers=headers, data=payload)
        if response.status_code != 200:
            return JsonResponse(
                {
                    "status": "Booking canceled successfully!, but failed to send Line notification."
                },
                status=200,
            )
        else:
            return JsonResponse(
                {
                    "status": "Booking canceled successfully and Line notification sent successfully!"
                },
                status=200,
            )

    return JsonResponse({"status": "Invalid request method."}, status=405)


def all_waiting_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(
                room__company=user_company, status__name="Waiting"
            ).order_by("created_at")
            context = {"room": room, "bookings": bookings, "url": "all_waiting"}
            return render(request, "room/waiting/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def all_approved_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(
                room__company=user_company, status__name="Approved"
            ).order_by("-created_at")
            context = {"room": room, "bookings": bookings, "url": "all_approved"}
            return render(request, "room/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def all_rejected_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(
                room__company=user_company, status__name="Rejected"
            ).order_by("-created_at")
            context = {"room": room, "bookings": bookings, "url": "all_rejected"}
            return render(request, "room/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def all_cancel_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(
                room__company=user_company, status__name="Canceled"
            ).order_by("-created_at")
            context = {"room": room, "bookings": bookings, "url": "all_cancel"}
            return render(request, "room/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def all_all_status_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            user_company = request.user.fccorp
            room_id = request.GET.get("room_id")
            room = Room.objects.filter(id=room_id).first()
            bookings = Booking.objects.filter(room__company=user_company).order_by(
                "-created_at"
            )
            context = {"room": room, "bookings": bookings, "url": "all_all_status"}
            return render(request, "room/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")
