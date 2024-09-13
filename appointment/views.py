from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Appointment, TakeAppointment
from .serializers import AppointmentSerializer
from Aayutan.utils.api_response import ApiResponse
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


@api_view(['POST'])
def update_appointment(request):
    appointment_id = request.data.get['appointment_id']

    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    new_address = request.data.get['new_address']
    new_start_time = request.data.get['new_start_time']


@api_view(['POST'])
def add_appointment(request):
    # TODO : request.user should be a doctor
    appointment = Appointment.objects.create(
        doctor=request.user,
        appointment_days=request.data.get('appointment_days'),
        address=request.data.get('address'),
        start_time=request.data.get('start_time'),
    )

    res_data = AppointmentSerializer(appointment).data
    response = ApiResponse(status='success', status_code=201,
                           message='Appointment created successfully', data=res_data)
    return Response(status=status.HTTP_201_CREATED, data=response.to_dict())


def get_my_appointments(request, pk=None):
    response = None
    if pk is not None:
        # Fetch a single appointment details
        appointment = TakeAppointment.objects.get(id=pk)
        res_data = AppointmentSerializer(appointment)
        response = ApiResponse(
            status='success', status_code=200, message='Appointment with ', data=res_data)
    else:
        # Fetch all appointments
        appointments = TakeAppointment.objects.filter(
            appointment__doctor=request.user)
        res_data = AppointmentSerializer(appointments, many=True).data
        response = ApiResponse(
            status='success', status_code=200, message='All appointments', data=res_data)
    return Response(status=status.HTTP_200_OK, data=response.to_dict())


def delete_appointment():
    pass
