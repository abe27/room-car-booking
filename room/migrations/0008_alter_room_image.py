# Generated by Django 5.0.4 on 2024-08-14 06:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("room", "0007_booking_created_at_booking_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="image",
            field=models.ImageField(blank=True, default="", upload_to="uploads/room/"),
        ),
    ]
