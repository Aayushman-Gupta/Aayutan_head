from django.contrib import admin
from django.urls import path
from .views import PatientLoginView,PatientLogoutView,PatientRegistrationView,DoctorLoginView,DoctorLogoutView,DoctorRegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('p/register/',PatientRegistrationView.as_view(), name='register'),
    path('d/register/',DoctorRegistrationView.as_view(), name='register'),
    path('p/login/', PatientLoginView.as_view(), name='login'),
    path('d/login/', DoctorLoginView.as_view(), name='login'),
    path('p/logout/', PatientLogoutView.as_view(), name='logout'),
    path('d/logout/', DoctorLogoutView.as_view(), name='logout'),
]
