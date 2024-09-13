from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # doctor urls
    path('add/', views.add_appointment),
    path('update/', views.update_appointment),
    path('get-my-appointments/', views.get_my_appointments),
    path('get-my-appointment/<str:id>/', views.get_my_appointments),
    path('delete/', views.delete_appointment),
    # patient urls
    path('take/', views.take_appointment),
    path('cancel-appointment/', views.cancel_appointment),
    path('get-patient-appointment/<str:id>/', views.get_patient_appointments),
    path('get-patient-appointments/', views.get_patient_appointments),
]
