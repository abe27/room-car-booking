from django.shortcuts import redirect, get_object_or_404  # type: ignore
from room.models import Booking, Status
from django.contrib import messages  # type: ignore


def edit_booking(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            # Get the booking ID from the form data
            booking_id = request.POST.get("id")
            status_id = request.POST.get("status")
            remark = request.POST.get("remark")

            # Get the booking object by its ID
            booking = get_object_or_404(Booking, id=booking_id)

            # Get the status object by its ID
            status = get_object_or_404(Status, id=status_id)

            # Update the booking fields
            booking.status = status
            booking.remark = remark
            booking.save()

            # Add a success message
            messages.success(request, "การจองได้รับการแก้ไขเรียบร้อยแล้ว")

            # Redirect to the bookings page (or wherever you want after editing)
            return redirect(
                "room_history_staff"
            )  # Change 'bookings_history' to the appropriate URL name

    # If not POST, just redirect or handle accordingly
    return redirect("/")
