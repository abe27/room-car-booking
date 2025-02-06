from room.models import Booking
from django.shortcuts import render
from django.utils import timezone

def list(request):
    today = timezone.now().date()  # Get today's date
    bookings = Booking.objects.filter(
        room__company=request.user.fccorp,
        status__sequence__in=[1, 4],
        start_date__date__gte=today  # Filter bookings starting today or later
        # start_date__date=today  # Filter bookings starting today
    ).order_by("start_date")[:15]
    context = {"bookings": bookings}
    return render(request, "room/room/list/index.html", context)

def card(request):
    today = timezone.now().date()  # Get today's date
    bookings = Booking.objects.filter(
        room__company=request.user.fccorp,
        status__sequence__in=[1, 4],
        start_date__date__gte=today  # Filter bookings starting today or later
        # start_date__date=today  # Filter bookings starting today
    ).order_by("start_date")[:15]
    context = {"bookings": bookings}
    return render(request, "room/room/card/index.html", context)