from django.contrib.auth.models import User
from django.db import models

import uuid
from django.utils import timezone



class DeviceInstance(models.Model):
    name = models.TextField(blank=True, help_text="short item name")
    model_curi = "lara:material_store/DeviceInstance"
    deviceinstance_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to="material_store/device_instance", blank=True, null=True, help_text="rel. path/filename to image"
    )


    def __str__(self):
        return self.name or ""

    def __repr__(self):
        return self.name or ""


class CalendarAbstract(models.Model):
    title = models.TextField(blank=True, help_text="title of the calendar entry")
    description = models.TextField(blank=True, help_text="text of the calendar entry")
    datetime_start = models.DateTimeField(
        default=timezone.now, help_text="start date & time of the event. RFC 5545 - DTSTART"
    )
    datetime_end = models.DateTimeField(default=timezone.now, help_text="end datetime of the event. RFC 5545 - DTEND")
    duration = models.TextField(
        blank=True,
        help_text=""" This value type is used to identify properties that contain
         a duration of time. RFC 5545 - DURATION""",
    )
    timestamp = models.TextField(max_length=100, default=timezone.now, help_text="timestamp of the event") 

    def __str__(self):
        return self.title or ""

    def __repr__(self):
        return self.title or ""

    class Meta:
        abstract = True


class DeviceBookingCalendar(CalendarAbstract):
    model_curi = "lara:material_store/DeviceBookingCalendar"
    devicebookingcalendar_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_user_related",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="LARA User, who created the calendar entry",
    )

    device_instance = models.ForeignKey(
        DeviceInstance,
        related_name="%(app_label)s_%(class)s_device_related",
        related_query_name="%(app_label)s_%(class)s_device_related_query",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Device to be booked",
    )
