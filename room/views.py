from django.shortcuts import render
from .models import Booking
import json

# Create your views here.
def room(request):
    bookings = Booking.objects.all()
    events = []
    for booking in bookings:
        events.append(
            {
                "title": booking.title,
                "start": booking.start_date.isoformat(),
                "end": booking.end_date.isoformat(),
                "description": booking.description,
                "color": (
                    booking.color.name if booking.color else "blue"
                ),  # Use a default color if not set
            }
        )
    context = {
        "events": json.dumps(events),  # แปลง events เป็น JSON
    }
    return render(request, "room/index.html", context)
