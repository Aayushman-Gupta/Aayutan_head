from rest_framework import serializers
from .models import Appointment, Day, TakeAppointment
from health_app.models import Doctor

from accounts.serializers import DoctorSerializer


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'name']


class AppointmentSerializer(serializers.ModelSerializer):
    # doctor = DoctorSerializer(read_only=True)
    # doctor_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Doctor.objects.all(), source='doctor', write_only=True)
    appointment_days = DaySerializer(many=True, read_only=True)
    class Meta:
        model = Appointment
        fields = ['id','appointment_days','address', 'start_time']


class TakeAppointmentSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer()

    class Meta:
        model = TakeAppointment
        fields = ['appointment', 'phone_number', 'date']
