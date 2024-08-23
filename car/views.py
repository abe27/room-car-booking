from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.http import JsonResponse, HttpResponseBadRequest # type: ignore
from .models import Car_Status, Car, Booking, Booking_Status, Location

# from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import requests # type: ignore


def profile(request):
    if request.user.is_authenticated:
        car_id = request.GET.get("car_id")
        car = Car.objects.filter(id=car_id).first()
        context = {"car": car, "url": "profile"}
        return render(request, "car/profile/index.html", context)
    else:
        return redirect("/")


def car(request):
    if request.user.is_authenticated:
        user_company = request.user.fccorp
        car_Status = Car_Status.objects.get(name="Active")
        cars = Car.objects.filter(company=user_company, status=car_Status).order_by(
            "sequence"
        )
        context = {
            "cars": cars,
            "default_car": cars[0] if cars.exists() else None,  # เพิ่ม default_car
        }
        return render(request, "car/home/index.html", context)
    else:
        return redirect("/")


def booking(request):
    if request.user.is_authenticated:
        car_id = request.GET.get("car_id")
        locations = Location.objects.all()  # ดึงข้อมูล location ทั้งหมดจากฐานข้อมูล
        car = Car.objects.filter(id=car_id).first()
        context = {"car": car, "locations": locations, "url": "booking"}
        return render(request, "car/booking/index.html", context)
    else:
        return redirect("/")


def calendar(request):
    if request.user.is_authenticated:
        car_id = request.GET.get("car_id")
        car = Car.objects.filter(id=car_id).first()
        context = {"car": car, "url": "calendar"}
        return render(request, "car/calendar/index.html", context)
    else:
        return redirect("/")


def fetch_bookings(request):
    car_id = request.GET.get("car_id")
    statuses = Booking_Status.objects.filter(name__in=["Waiting", "Approved"])
    bookings = Booking.objects.filter(car_id=car_id, status__in=statuses)
    booking_data = []
    for booking in bookings:
        booking_data.append(
            {
                "id": booking.pk,
                "emp_id": booking.employee.emp_id,
                "first_name": booking.employee.first_name,
                "last_name": booking.employee.last_name,
                "title": booking.title,
                "location": booking.location.name,
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
        data = request.POST
        title = data.get("title")
        company = request.user.fccorp
        location_id = data.get("location")
        description = data.get("description")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # Retrieve the Location instance
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return JsonResponse(
                {"status": "Location not found."},
                status=404,
            )

        # Validate dates
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

        employee = request.user
        status = Booking_Status.objects.get(name="Waiting")

        # Save the booking
        booking = Booking.objects.create(
            employee=employee,
            title=title,
            company=company,
            location=location,
            description=description,
            start_date=start_date_iso,
            end_date=end_date_iso,
            status=status,
        )

        # Send Line Notify
        line_notify_token = request.user.fccorp.line_notify_car
        line_notify_url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        message = f"\nBooking ID: {booking.id}\nTitle: {booking.title}\nRequester: {booking.employee.first_name} {booking.employee.last_name}\nLocation: {booking.location.name}\nDescription: {booking.description}\nTel: {booking.employee.tel}\nStart: {booking.start_date}\nEnd: {booking.end_date}\nStatus: {booking.status.name}"
        payload = {"message": message}

        response = requests.post(line_notify_url, headers=headers, data=payload)
        if response.status_code != 200:
            return JsonResponse(
                {"status": "Booking saved, but failed to send Line notification."},
                status=200,
            )
        else:
            return JsonResponse(
                {"status": "Booking saved and Line notification sent successfully!"},
                status=200,
            )

    return JsonResponse({"status": "Invalid request"}, status=400)


def cancel_booking(request):
    booking_id = request.POST.get("id")
    booking = get_object_or_404(Booking, id=booking_id, employee=request.user)
    booking.status = Booking_Status.objects.get(name="Canceled")
    booking.save()

    return JsonResponse({"success": True})


def history(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        company_id = request.user.fccorp.id
        car_id = request.GET.get("car_id")
        car = Car.objects.filter(id=car_id).first()
        bookings = Booking.objects.filter(
            employee__id=user_id, company__id=company_id
        ).order_by("-created_at")
        context = {"car": car, "bookings": bookings, "url": "history"}
        return render(request, "car/history/index.html", context)
    else:
        return redirect("/")


def all_status(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            company_id = request.user.fccorp.id
            car_id = request.GET.get("car_id")
            bookings = Booking.objects.filter(
                company__id=company_id, car__id=car_id
            ).order_by("-created_at")
            context = {"car": car, "bookings": bookings, "url": "all_status"}
            return render(request, "car/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def approve_booking(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)

        # Set the status to Approved
        approved_status = get_object_or_404(Booking_Status, name="Approved")
        booking.status = approved_status

        # Assign the approver as the current logged-in user
        booking.approver = request.user

        # Parse the JSON body to get the remark and car_id
        data = json.loads(request.body)
        remark = data.get("remark", "").strip()
        car_id = data.get("car_id")

        # Validate and assign the selected car to the booking
        if car_id:
            car = get_object_or_404(Car, id=car_id)
            booking.car = car
        else:
            return JsonResponse("Invalid car selection")

        booking.remark = remark
        booking.save()

        # Send Line Notify
        line_notify_token = request.user.fccorp.line_notify_car
        line_notify_url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        message = f"\nBooking ID: {booking.id}\nCar: {booking.car.name}\nTitle: {booking.title}\nRequester: {booking.employee.first_name} {booking.employee.last_name}\nLocation: {booking.location.name}\nDescription: {booking.description}\nTel: {booking.employee.tel}\nStart: {booking.start_date}\nEnd: {booking.end_date}\nRemark: {booking.remark}\nStatus: {booking.status.name}"
        payload = {"message": message}

        response = requests.post(line_notify_url, headers=headers, data=payload)
        if response.status_code != 200:
            return JsonResponse(
                {"status": "Booking approved, but failed to send Line notification."},
                status=200,
            )
        else:
            return JsonResponse(
                {"status": "Booking approved and Line notification sent successfully!"},
                status=200,
            )
    else:
        return HttpResponseBadRequest("Invalid request method")


def reject_bookings(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)

        # Get the status for Rejected
        rejected_status = get_object_or_404(Booking_Status, name="Rejected")
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
        line_notify_token = request.user.fccorp.line_notify_car
        line_notify_url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        message = f"\nBooking ID: {booking.id}\nTitle: {booking.title}\nRequester: {booking.employee.first_name} {booking.employee.last_name}\nLocation: {booking.location.name}\nDescription: {booking.description}\nTel: {booking.employee.tel}\nStart: {booking.start_date}\nEnd: {booking.end_date}\nRemark: {booking.remark}\nStatus: {booking.status.name}"
        payload = {"message": message}

        response = requests.post(line_notify_url, headers=headers, data=payload)
        if response.status_code != 200:
            return JsonResponse(
                {"status": "Booking rejected, but failed to send Line notification."},
                status=200,
            )
        else:
            return JsonResponse(
                {"status": "Booking rejected and Line notification sent successfully!"},
                status=200,
            )

    return JsonResponse({"status": "Invalid request method."}, status=405)


def staff_cancel_bookings(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)

        # Get the status for Rejected
        canceled_status = get_object_or_404(Booking_Status, name="Canceled")
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
        line_notify_token = request.user.fccorp.line_notify_car
        line_notify_url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        message = f"\nBooking ID: {booking.id}\nCar: {booking.car.name}\nTitle: {booking.title}\nRequester: {booking.employee.first_name} {booking.employee.last_name}\nLocation: {booking.location.name}\nDescription: {booking.description}\nTel: {booking.employee.tel}\nStart: {booking.start_date}\nEnd: {booking.end_date}\nRemark: {booking.remark}\nStatus: {booking.status.name}"
        payload = {"message": message}

        response = requests.post(line_notify_url, headers=headers, data=payload)
        if response.status_code != 200:
            return JsonResponse(
                {"status": "Booking canceled, but failed to send Line notification."},
                status=200,
            )
        else:
            return JsonResponse(
                {"status": "Booking canceled and Line notification sent successfully!"},
                status=200,
            )

    return JsonResponse({"status": "Invalid request method."}, status=405)


def all_waiting_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            company_id = request.user.fccorp.id
            car_id = request.GET.get("car_id")
            car = Car.objects.filter(id=car_id).first()
            cars = Car.objects.filter(company_id=company_id)
            bookings = Booking.objects.filter(
                company__id=company_id, status__name="Waiting"
            ).order_by("created_at")
            context = {
                "car": car,
                "cars": cars,
                "bookings": bookings,
                "url": "all_waiting",
            }
            return render(request, "car/waiting/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def all_approved_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            company_id = request.user.fccorp.id
            car_id = request.GET.get("car_id")
            car = Car.objects.filter(id=car_id).first()
            bookings = Booking.objects.filter(
                company__id=company_id, status__name="Approved"
            ).order_by("-created_at")
            context = {"car": car, "bookings": bookings, "url": "all_approved"}
            return render(request, "car/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def all_rejected_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            company_id = request.user.fccorp.id
            car_id = request.GET.get("car_id")
            car = Car.objects.filter(id=car_id).first()
            bookings = Booking.objects.filter(
                company__id=company_id, status__name="Rejected"
            ).order_by("-created_at")
            context = {"car": car, "bookings": bookings, "url": "all_rejected"}
            return render(request, "car/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def all_cancel_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            company_id = request.user.fccorp.id
            car_id = request.GET.get("car_id")
            car = Car.objects.filter(id=car_id).first()
            bookings = Booking.objects.filter(
                company__id=company_id, status__name="Canceled"
            ).order_by("-created_at")
            context = {"car": car, "bookings": bookings, "url": "all_cancel"}
            return render(request, "car/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def all_all_status_bookings(request):
    if request.user.is_authenticated:
        # if request.user.fcdept.fcname == "HR" or request.user.fcdept.fcname == "IT":
        if request.user.is_staff == True:
            company_id = request.user.fccorp.id
            car_id = request.GET.get("car_id")
            car = Car.objects.filter(id=car_id).first()
            bookings = Booking.objects.filter(company__id=company_id).order_by(
                "-created_at"
            )
            context = {"car": car, "bookings": bookings, "url": "all_all_status"}
            return render(request, "car/approve/index.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")
