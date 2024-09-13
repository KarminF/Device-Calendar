from django.contrib import admin

# Register your models here.

from .models import DeviceInstance, DeviceBookingCalendar


admin.site.register(DeviceInstance)

admin.site.register(DeviceBookingCalendar)





