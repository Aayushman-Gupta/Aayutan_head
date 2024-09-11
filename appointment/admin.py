from django.contrib import admin
from .models import Appointment,TakeAppointment,Day

# Register your models here.
admin.site.register(Appointment)
admin.site.register(TakeAppointment)
admin.site.register(Day)