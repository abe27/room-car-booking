from room.models import Booking
from django.shortcuts import render
from django.utils import timezone

def index(request):
    today = timezone.now().date()  # Get today's date
    bookings = Booking.objects.filter(
        room__company=request.user.fccorp,
        start_date__date=today  # Filter bookings starting today
    ).order_by("start_date")
    context = {"bookings": bookings}
    return render(request, "room/room/index.html", context)
