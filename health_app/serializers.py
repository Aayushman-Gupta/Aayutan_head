from rest_framework import serializers
from health_app.models import Patient,Doctor

class PatientSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    # password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = ['username','password']


    
    def create(self, validated_data):
        user = Patient(
            username=validated_data['username'],
        )   
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name'] 