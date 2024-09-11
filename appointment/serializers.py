from rest_framework import serializers
from .models import Appointment,Day
from health_app.models import Doctor

from health_app.serializers import DoctorSerializer
class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'name'] 
        

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), source='doctor', write_only=True)
    appointment_days = DaySerializer(many=True, read_only=True)
    appointment_days_ids = serializers.PrimaryKeyRelatedField(queryset=Day.objects.all(), many=True, source='appointment_days', write_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'doctor_id', 'appointment_days', 'appointment_days_ids', 'location', 'start_time', 'end_time', 'created_at']