from room.models import Booking
from django.shortcuts import render, redirect
from django.utils import timezone


def list(request):
    if request.user.is_authenticated:
        today = timezone.now().date()  # Get today's date
        bookings = Booking.objects.filter(
            room__company=request.user.fccorp,
            status__sequence__in=[1, 4],
            start_date__date__gte=today,  # Filter bookings starting today or later
            # start_date__date=today  # Filter bookings starting today
        ).order_by("start_date")[:15]
        context = {"bookings": bookings}
        return render(request, "room/room/list/index.html", context)
    else:
        return redirect("/")


def card(request):
    if request.user.is_authenticated:
        today = timezone.now().date()  # Get today's date
        bookings = (
            Booking.objects.filter(
                room__company=request.user.fccorp,
                status__sequence__in=[1, 4],
                start_date__date=today,  # Filter bookings starting today
            )
            .order_by("start_date", "end_date")[:15]
        )
        context = {"bookings": bookings}
        return render(request, "room/room/card/index.html", context)
    else:
        return redirect("/")
    
# def card(request):
#     if request.user.is_authenticated:
#         today = timezone.now().date()  # Get today's date
#         bookings = (
#             Booking.objects.filter(
#                 room__company=request.user.fccorp,
#                 status__sequence__in=[1, 4],
#                 start_date__date=today,  # Filter bookings starting today
#             )
#             .distinct("room")
#             .order_by("room", "start_date")
#         )
#         context = {"bookings": bookings}
#         return render(request, "room/room/card/index.html", context)
#     else:
#         return redirect("/")
