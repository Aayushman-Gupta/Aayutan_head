from django.db import models
from health_app.models import Doctor,Patient
from django.utils import timezone
# Create your models here.

class Day(models.Model):
    day_choices=[
        ("Monday","MON"),
        ("Tuesday","TUE"),
        ("Wednesday","WED"),
        ("Thursday","THU"),
        ("Friday","FRI"),
        ("Saturday","SAT"),
        ("Sunday","SUN")
    ]
    name = models.CharField(choices=day_choices, unique=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    # user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,max_length=100,on_delete=models.CASCADE)
    appointment_days=models.ManyToManyField(Day)
    location = models.CharField(max_length=100)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    # hospital_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    # def get_absolute_url(self):
    # return reverse('appointment:delete-appointment', kwargs={'pk': self.pk})
    

class TakeAppointment(models.Model):
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    # full_name = models.CharField(max_length=100)
    # message = models.TextField()
    phone_number = models.CharField(max_length=15)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name
