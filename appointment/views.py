from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Appointment, TakeAppointment, Day
from .serializers import AppointmentSerializer, TakeAppointmentSerializer
from Aayutan.utils.api_response import ApiResponse
from rest_framework.response import Response
from rest_framework import status
from health_app.models import Doctor, Patient
# Create your views here.


# ********************************
# **ADD AN APPOINTMENT*********
# ********************************

@api_view(['POST'])
def add_appointment(request):
    doctor = request.user
    print(doctor)
    print(doctor.id)
    print(doctor.username)
    serializer = AppointmentSerializer(data=request.data)
    
    if serializer.is_valid():
    # A list of days (e.g., ['Monday', 'Tuesday', 'Wednesday'])
        days = [Day.objects.get_or_create(name=day)[0]
                for day in request.data.get('days')]
        print(days)
        start_time = request.data.get('start_time')
        address = request.data.get('address')
        try:
            doctor = Doctor.objects.get(username=doctor.username)
            appointments = []
            for day in days:
                appointments.append(Appointment(
                    doctor=doctor,
                    day=day,
                    start_time=start_time,
                    address=address
                ))

            Appointment.objects.bulk_create(appointments)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'success': 'Appointments created successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 # UPDATE ANY APPOINTMENT


@api_view(['PUT'])
def update_appointment(request):
    appointment_id = request.data.get('appointment_id')
    new_address = request.data.get('new_address')
    new_start_time = request.data.get('new_start_time')

    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if new_start_time:
            appointment.start_time = new_start_time
        if new_address:
            appointment.address = new_address
        appointment.save()
        data = AppointmentSerializer(appointment).data
        data['success']='Appointment updated successfully'
        response=ApiResponse(status='success',status_code=200,data=data)
        return Response(status=status.HTTP_200_OK, data=response.to_dict())

    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_my_appointments(request, pk=None):
    
#URL to check on POSTMAN::"http://127.0.0.1:8000/appointment/get-my-appointments/?username=Aayushman"
    try:
        if pk is not None:
            # Fetch a single appointment details
            appointment = Appointment.objects.get(id=pk)
            res_data = AppointmentSerializer(appointment)
            response = ApiResponse(
                status='success', status_code=200, message='Appointment with ', data=res_data)
        else:
            username = request.query_params.get('username') 
            if username is None:
                    return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
 
            # Fetch all appointments
            appointments = Appointment.objects.filter(doctor__username=username)
            
            if not appointments.exists():
                    return Response({'error': 'No appointments found'}, status=status.HTTP_404_NOT_FOUND)
                
            res_data = AppointmentSerializer(appointments, many=True).data
            response = ApiResponse(
                status='success', status_code=200, message='All appointments', data=res_data)
        return Response(status=status.HTTP_200_OK, data=response.to_dict())
    
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])

# URL for delete path::"http://127.0.0.1:8000/appointment/delete/2/"

def delete_appointment(request, id):
    try:
        appointment = Appointment.objects.get(id=id)
        appointment.delete()
        return Response({'message': 'Appointment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST']) 
def take_appointment(request):
    # Get the patient ID and appointment ID from the request
    patient_id = request.data.get('patient_id')
    appointment_id =request.data.get('appointment_id')
    phone_number = request.data.get('phone_number')

    if not patient_id or not appointment_id or not phone_number:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if patient exists
    try:
        patient = Patient.objects.get(id=patient_id)
        
        # Check if the appointment exists or not
        appointment = Appointment.objects.get(id=appointment_id)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if TakeAppointment.objects.filter(appointment=appointment).exists():
            return Response({'error': 'Appointment already taken'}, status=status.HTTP_400_BAD_REQUEST)

    TakeAppointment.objects.create(
            patient=patient,
            appointment=appointment,
            phone_number=phone_number
        )
    return Response({'success': 'Appointment successfully booked'}, status=status.HTTP_201_CREATED)
      


@api_view(['DELETE'])
def cancel_appointment(request,patient_id,appointment_id):
    
    # URL for testing::"http://127.0.0.1:8000/appointment/cancel-appointment/3/3/"
    
    # Get the patient ID and appointment ID from the request
    try:
        patient = Patient.objects.get(id=patient_id)
        appointment = Appointment.objects.get(id=appointment_id)
        booking = TakeAppointment.objects.get(
            patient=patient, appointment=appointment)
        booking.delete()

    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    except TakeAppointment.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'success': 'Appointment successfully cancelled'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_patient_appointments(request):
    #URL to check ::"http://127.0.0.1:8000/appointment/get-patient-appointments/?username=aayushman123"
    username=request.query_params.get('username')
    
    patient_appointments = TakeAppointment.objects.filter(patient__username=username)
    res_data = TakeAppointmentSerializer(patient_appointments, many=True).data
    api_response = ApiResponse(
        status='success', status_code=200, data=res_data)
    return Response(status=status.HTTP_200_OK, data=api_response.to_dict())


@api_view(['GET'])
def get_scheduled_appointments(request):
    scheduled_appointments = TakeAppointment.objects.filter(
        appointment__doctor=request.user)
    response = TakeAppointmentSerializer(
        scheduled_appointments, many=True).data
    api_response = ApiResponse(status='success', status_code=200,
                               data=response, message='All scheduled appointments')
    return Response(status=status.HTTP_200_OK, data=api_response.to_dict())