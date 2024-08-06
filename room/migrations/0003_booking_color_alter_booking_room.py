# Generated by Django 5.0.7 on 2024-08-06 06:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("room", "0002_color_alter_room_image_alter_room_name_booking"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="color",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bookings",
                to="room.color",
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="room",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bookings",
                to="room.room",
            ),
        ),
    ]
