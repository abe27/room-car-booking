import requests
from django.utils import timezone
from datetime import timedelta
from .models import Booking
from django.utils.timezone import localtime


def notify_upcoming_bookings():
    now = timezone.now()
    upcoming_time = now + timedelta(minutes=30)
    bookings = Booking.objects.filter(
        start_date__lte=upcoming_time, end_date__gte=now, status__name="Approved"
    )

    for booking in bookings:
        local_start = localtime(booking.start_date)  # แปลงเป็นเวลาท้องถิ่น
        local_end = localtime(booking.end_date)  # แปลงเป็นเวลาท้องถิ่น

        message = (
            f"\n🔔 แจ้งเตือน: อีกประมาณ 30 นาทีท่านจะถึงเวลาจองห้องประชุม\n"
            f"ห้อง: {booking.room.name}\n"
            f"หัวข้อ: {booking.title}\n"
            f"ผู้จอง: {booking.employee.first_name} {booking.employee.last_name}\n"
            f"คำอธิบาย: {booking.description}\n"
            f"เบอร์โทร: {booking.employee.tel}\n"
            f"เริ่ม: {local_start.strftime('%d/%m/%Y %H:%M')}\n"
            f"สิ้นสุด: {local_end.strftime('%d/%m/%Y %H:%M')}\n"
            f"สถานะ: {booking.status.name}\n"
        )

        payload = {"message": message}
        line_notify_token = booking.employee.fccorp.line_notify_room
        line_notify_url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        response = requests.post(line_notify_url, headers=headers, data=payload)
        if response.status_code != 200:
            print(f"Failed to send Line notification for booking {booking.id}")
