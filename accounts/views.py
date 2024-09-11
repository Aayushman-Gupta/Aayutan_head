from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from health_app.serializers import PatientSerializer
from rest_framework import serializers
from health_app.models import Patient
from health_app.tokens import get_token_for_user


class UserRegistrationView(APIView):

    # The line `permission_classes = [AllowAny]` in the `UserRegistrationView` class is setting the
    # permission classes for the view. In this case, `[AllowAny]` means that the view does not require
    # authentication or any specific permissions to access it. It allows any user, authenticated or
    # not, to make requests to this view.
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        # patient=Patient(username=username)
        # patient.set_password(password)

        # refresh=RefreshToken.for_user(patient)

        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Get token for user
            token = get_token_for_user(user)

            return Response({
                'message': 'User registered successfully',
                'user': PatientSerializer(user).data,
                'token': token
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Generate JWT tokens
                token = get_token_for_user(user)
                return Response({
                    'token': token
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    # permission_classes = [IsAuthenticated] Commented cause it is default

    def post(self, request, *args, **kwargs):
        try:
            # Extract the refresh token from the request data
            refresh_token = request.data.get('refresh_token')

            if refresh_token is None:
                return Response({'error': 'Refresh token is required'}, status=400)

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'User logged out successfully'}, status=205)

        except Exception as e:
            return Response({'error': str(e)}, status=400)
