from rest_framework import serializers
from health_app.models import Patient

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
    # def validate(self, data):
    #     if data['password'] != data['password_confirmation']:
    #         raise serializers.ValidationError({"password_confirmation": "Passwords must match."})
    #     return data

    # def create(self, validated_data):
    #     validated_data.pop('password_confirmation', None)
    #     patient = Patient.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #         date_of_birth=validated_data['date_of_birth'],
    #         gender=validated_data['gender'],
    #         address=validated_data['address'],
    #         phone_number=validated_data['phone_number'],
    #         password=validated_data['password']
    #     )
    #     return patient