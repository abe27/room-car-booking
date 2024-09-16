import requests
from datetime import timedelta
from .models import Booking
from django.utils.timezone import localtime
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(notify_upcoming_bookings, 'interval', minutes=10)
    trigger = CronTrigger(
        hour="7-17", minute="*/10"
    )  # Run every 10 minutes between 07:00 and 17:00
    scheduler.add_job(notify_upcoming_bookings, trigger)
    scheduler.start()


def test():
    print("I love python {}".format(datetime.now()))


def notify_upcoming_bookings():
    print("Notify Upcoming Bookings:", datetime.now())
    now = datetime.now()
    upcoming_time = now + timedelta(minutes=30)
    bookings = Booking.objects.filter(
        start_date__lte=upcoming_time,
        end_date__gte=now,
        status__sequence=1,  # sequence 1 = Approved
        message=0,
    )

    for booking in bookings:
        local_start = localtime(booking.start_date)  # แปลงเป็นเวลาท้องถิ่น
        local_end = localtime(booking.end_date)  # แปลงเป็นเวลาท้องถิ่น
        confirm_url = f"http://127.0.0.1:8000/room/confirm_booking/{booking.id}"

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
            f"โปรดกดลิ้งค์ด้านล่างนี้เพื่อยืนยันการเข้าห้องประชุม\n"
            f"{confirm_url}\n"
        )

        payload = {"message": message}
        line_notify_token = booking.employee.fccorp.line_notify_room
        line_notify_url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        response = requests.post(line_notify_url, headers=headers, data=payload)

        if response.status_code == 200:
            # If the notification is successfully sent, update the message status
            booking.message = 1
            booking.save()
        else:
            print(f"Failed to send Line notification for booking {booking.id}")
