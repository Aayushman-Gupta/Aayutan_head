from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Appointment, TakeAppointment
from .serializers import AppointmentSerializer, TakeAppointmentSerializer
from Aayutan.utils.api_response import ApiResponse
from rest_framework.response import Response
from rest_framework import status
from health_app.models import Doctor, Patient
# Create your views here.


# ********************************
# ***ADD AN APPOINTMENT**********
# ********************************

@api_view(['POST'])
def add_appointment(request):
    doctor_id = request.data.get('doctor_id')
    # A list of days (e.g., ['Monday', 'Tuesday', 'Wednesday'])
    days = request.data.get('days')
    start_time = request.data.get('start_time')
    address = request.data.get('address')
    try:
        doctor = Doctor.objects.get(id=doctor_id)
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
        response = AppointmentSerializer(appointment).data

    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'success': 'Appointment updated successfully'}, status=status.HTTP_200_OK, data=response.data)


@api_view(['GET'])
def get_my_appointments(request, pk=None):
    response = None
    if pk is not None:
        # Fetch a single appointment details
        appointment = Appointment.objects.get(id=pk)
        res_data = AppointmentSerializer(appointment)
        response = ApiResponse(
            status='success', status_code=200, message='Appointment with ', data=res_data)
    else:
        # Fetch all appointments
        appointments = Appointment.objects.filter(
            doctor=request.user)
        res_data = AppointmentSerializer(appointments, many=True).data
        response = ApiResponse(
            status='success', status_code=200, message='All appointments', data=res_data)
    return Response(status=status.HTTP_200_OK, data=response.to_dict())


@api_view(['DELETE'])
def delete_appointment(request):
    appointment_id = request.data.get('appointment_id')

    if not appointment_id:
        return Response({'error': 'Appointment ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Get the appointment by ID
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.delete()
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'success': 'Appointment deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def take_appointment(request):
    # Get the patient ID and appointment ID from the request
    patient_id = request.data.get('patient_id')
    appointment_id = request.data.get('appointment_id')
    phone_number = request.data.get('phone_number')

    # Check if patient exists
    try:
        patient = Patient.objects.get(id=patient_id)

        # Check if the appointment exists or not
        appointment = Appointment.objects.get(id=appointment_id)
        if TakeAppointment.objects.filter(appointment=appointment).exists():
            return Response({'error': 'Appointment already taken'}, status=status.HTTP_400_BAD_REQUEST)

        take_appointment = TakeAppointment.objects.create(
            user=patient,
            appointment=appointment,
            phone_number=phone_number
        )
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'success': 'Appointment successfully booked'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def cancel_appointment(request):
    # Get the patient ID and appointment ID from the request
    patient_id = request.data.get('patient_id')
    appointment_id = request.data.get('appointment_id')

    try:
        patient = Patient.objects.get(id=patient_id)
        booking = TakeAppointment.objects.get(
            user=patient, appointment_id=appointment_id)
        booking.delete()

    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    except TakeAppointment.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'success': 'Appointment successfully canceled'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_patient_appointments(request):
    patient_appointments = TakeAppointment.objects.filter(user=request.user)
    res_data = TakeAppointmentSerializer(patient_appointments, many=True).data
    api_response = ApiResponse(
        status='success', status_code=200, data=res_data.to_dict())
    return Response(status=status.HTTP_200_OK, data=api_response)


@api_view(['GET'])
def get_scheduled_appointments(request):
    scheduled_appointments = TakeAppointment.objects.filter(
        appointment__doctor=request.user)
    response = TakeAppointmentSerializer(
        scheduled_appointments, many=True).data
    api_response = ApiResponse(status='success', status_code=200,
                               data=response, message='All scheduled appointments')
    return Response(status=status.HTTP_200_OK, data=api_response.to_dict())
